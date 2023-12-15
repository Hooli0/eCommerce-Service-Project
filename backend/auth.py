#Functions related to authorisation of client
import random
import string
import re
import hashlib
import jwt
import json
import database
from datetime import datetime

def generate_token(user_id, dt):
    '''
        Creates a jwt token with the secret based off the u_id and password of the user
    '''
    secret_code = 'secret'
    encoded = jwt.encode({"user_id": user_id, "datetime": dt}, secret_code, algorithm='HS256')

    return str(encoded)

def decode_token(token):
    '''
        Decode token will take a token, validate the token by
        checking valid_tokens.txt and return the decoded token
    '''
    token = token.strip('\"')
    secret_code = 'secret'
    decoded_token = jwt.decode(token, secret_code, algorithms=['HS256']) 

    return decoded_token
    

def auth_register_admin(first_name, last_name, username, email, password, client_collection, client_tokens):
    '''
        Registers an admin and adds them to the admin collection
    '''
    # Error checks values
    check = registry_check(email, username, password, client_collection)
    if(check['success'] is False):
        return check

    current_user_count = client_collection.find({}).collection.count_documents({})

    dt = str(datetime.now())
    # Generates token and saves it into token database
    generated_token = generate_token(current_user_count, dt)
    client_tokens.insert_one({"token": generated_token})
    # Creates dictionary of user details and adds it to database
    mydict = create_dict_admin(current_user_count, first_name, last_name, username, email, password, dt)
    client_collection.insert_one(mydict)

    return {
        'success': True,
        'token': generated_token
    }

def auth_register_user(first_name, last_name, username, email, password, client_collection, client_tokens):
    '''
        Registers a user and adds them to the user collection
    '''
    # Error checks values
    check = registry_check(email, username, password, client_collection)
    if(check['success'] is False):
        return check

    current_user_count = client_collection.find({}).collection.count_documents({})

    dt = str(datetime.now())
    # Generates token and saves it into admin_token database
    generated_token = generate_token(current_user_count, dt)
    client_tokens.insert_one({"token": generated_token})
    # Creates dictionary of user details and adds it to database
    mydict = create_dict_user(current_user_count, first_name, last_name, username, email, password, dt)
    client_collection.insert_one(mydict)

    return {
        'success': True,
        'token': generated_token
    }


def auth_login(username, password, client_collection, client_tokens):
    '''
        Checks the email and password of a user with the user_list and gives them a token
    '''

    password = hash_password(password)
    username_query = check_user_exists(username, client_collection)

    # If username does not exist or password does not match username, return failure
    if username_query is None or username_query["password"] != password:
        return {
            'success': False,
            'message': 'The credentials you have entered are incorrect.'
        }

    generated_token = ""
    if not username_query["logged_in"]:
        # Generate token
        dt = str(datetime.now())
        generated_token = generate_token(username_query["user_id"], dt)
        # Add token to token collection if token does not already exist
        if check_token_exists(generated_token, client_tokens) is False:
            client_tokens.insert_one({"token": generated_token})
        client_collection.update_one({"username": username}, {"$set": {"logged_in": True, "last_login_date": dt}})
    else:
        generated_token = generate_token(username_query["user_id"], username_query["last_login_date"])
        # This should be an error but im lazy
        if check_token_exists(generated_token, client_tokens) is False:
            return {
                'success': False,
                'message': 'Unable to reconstruct token.'
            }

    # Return token
    return {
        'success': True,
        'token': generated_token
    }

def auth_login(username, password, client_collection, client_tokens):
    '''
        Checks the email and password of a user with the user_list and gives them a token
    '''

    password = hash_password(password)
    username_query = check_user_exists(username, client_collection)

    # If username does not exist or password does not match username, return failure
    if username_query is None or username_query["password"] != password:
        return {
            'success': False,
            'message': 'The credentials you have entered are incorrect.'
        }

    generated_token = ""
    if not username_query["logged_in"]:
        # Generate token
        dt = datetime.now()
        dt_str = str(dt)
        
        generated_token = generate_token(username_query["user_id"], dt_str)
        # Add token to token collection if token does not already exist
        if check_token_exists(generated_token, client_tokens) is False:
            client_tokens.insert_one({"token": generated_token})
        client_collection.update_one({"username": username}, {"$set": {"logged_in": True, "last_login_date": dt_str}})
    else:
        generated_token = generate_token(username_query["user_id"], username_query["last_login_date"])
        # This should be an error but im lazy
        if check_token_exists(generated_token, client_tokens) is False:
            return {
                'success': False,
                'message': 'Unable to reconstruct token.'
            }

    # Return token
    return {
        'success': True,
        'token': generated_token
    }

def auth_logout(token, client_collection, client_tokens):
    '''
        Logs out a user provided the token matches
    '''

    # Checks if the token exists and returns a failure if it does not
    if check_token_exists(token, client_tokens) is False:
        return {
            'success': False,
            'message': 'User is not logged in.'
        }

    decoded = decode_token(token)
    user_id = decoded["user_id"]
    client_collection.update_one({"user_id": user_id}, {"$set": {"logged_in": False}})

    client_tokens.delete_one({"token": token})
    # Return
    return {
        'success': True
    }


'''
    Consider moving the below into a user.py file
'''

def get_admin_details(token, client_collection, client_tokens):
    '''
        Get user details from token
    '''
    id_query = get_user_with_token(token, client_collection)

    if id_query is None:
        return {
            'success': False,
            'message': 'User does not exist.'
        }

    # Add token to token collection if token does not already exist
    if check_token_exists(token, client_tokens) is False:
        return {
            'success': False,
            'message': 'User is not logged in.'
        }

    user_details = {
        'first_name': id_query['first_name'],
        'last_name': id_query['last_name'],
        'username': id_query['username'],
        'email': id_query['email'],
        'address': id_query['address']
    }

    # Return
    return {
        'success': True,
        'details': json.dumps(user_details)
    }

def get_user_details(token, client_collection, client_tokens):
    '''
        Get user details from token
    '''
    id_query = get_user_with_token(token, client_collection)

    if id_query is None:
        return {
            'success': False,
            'message': 'User does not exist.'
        }

    # Add token to token collection if token does not already exist
    if check_token_exists(token, client_tokens) is False:
        return {
            'success': False,
            'message': 'User is not logged in.'
        }

    cart = id_query['cart']
    for item in cart:
        print(item)
        print(item['item'])
        print(item['item']['_id'])
        del item['item']['_id']

    user_details = {
        'first_name': id_query['first_name'],
        'last_name': id_query['last_name'],
        'username': id_query['username'],
        'email': id_query['email'],
        'address': id_query['address'],
        'cart': id_query['cart'],
        'tag_data': id_query['tag_data']
    }

    # Return
    return {
        'success': True,
        'details': json.dumps(user_details)
    }

def change_username(new_username, token, client_collection, client_tokens):
    '''
        Change username of the user
    '''
    # If length of new username is longer than 16 characters
    if len(new_username) > 16:
        return {
            'success': False,
            'message': "Username is too long (Please make it below 16 characters)"
        }
    
    if check_token_exists(token, client_tokens) is False:
        return {
            'success': False,
            'message': 'User is not logged in.'
        }

    decoded = decode_token(token)
    user_id = decoded['user_id']
    user_id_query = client_collection.find_one({"user_id": int(user_id)})

    # If token is not valid, return faiure
    if user_id_query is None:
        return {
            'success': False,
            'message': "Invalid Token",
            'userID': user_id
        }

    # Edits current username to new username
    client_collection.update_one(user_id_query, {"$set": {"username": new_username}})

    # Return
    return {
        'success': True,
        'message': "Successfully changed username"
    }

def change_password(new_password, token, client_collection, client_tokens):
    '''
        Change password of the user
    '''
    if len(new_password) < 6:
        return {
            'success': False,
            'message': "Password is too short"
        }

    if check_token_exists(token, client_tokens) is False:
        return {
            'success': False,
            'message': 'User is not logged in.'
        }

    user_id_query = get_user_with_token(token, client_collection)
    # If token is not valid, return faiure
    if user_id_query is None:
        return {
            'success': False,
            'message': "Invalid Token"
        }

    # Edits current password to new password
    client_collection.update_one(user_id_query, {"$set": {"password": hash_password(new_password)}})

    # Return
    return {
        'success': True,
        'message': "Successfully changed password"
    }

def change_address(address, city, suburb, state, post_code, token, client_collection, client_tokens):
    '''
        Change address details
    '''
    user_id_query = get_user_with_token(token, client_collection)
    # If token is not valid, return faiure
    if user_id_query is None:
        return {
            'success': False,
            'message': "Invalid Token"
        }
    
    if check_token_exists(token, client_tokens) is False:
        return {
            'success': False,
            'message': 'User is not logged in.'
        }

    address_dict = {
        "address": address,
        "city": city,
        "suburb": suburb,
        "state": state,
        "post_code": post_code
    }

    # Edits current password to new password
    client_collection.update_one(user_id_query, {"$set": {"address": address_dict}})
    # Return
    return {
        'success': True,
        'message': "Successfully changed address"
    }

'''
    Helper functions
'''

def valid_email(email):
    '''
        Checks if the email is a valid email
    '''
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    return False

def hash_password(password):
    '''
        Hashes the password given
    '''
    return hashlib.sha256(password.encode()).hexdigest()

def check_token_exists(token, client_tokens):
    '''
        Checks if a token already exists
    '''
    same_token_check = {"token": token}
    token_query = client_tokens.find_one(same_token_check)

    if token_query is None:
        return False
    return True

def check_user_exists(username, client_collection):
    '''
        Checks if a user exists
    '''
    same_username_check = {"username": username }
    username_query = client_collection.find_one(same_username_check)

    # If username does not exist, return failure
    return username_query

def get_user_with_token(token, client_collection):
    '''
        Returns the user with the corresponding token
    '''
    decoded = decode_token(token)
    user_id = decoded['user_id']
    user_id_query = client_collection.find_one({"user_id": int(user_id)})

    return user_id_query

def create_dict_admin(current_user_count, first_name, last_name, username, email, password, dt):
    '''
        Creates and returns a dictionary for admin
    '''
    # Creates dictionary of user details and adds it to database
    mydict = {
        "user_id": current_user_count, 
        "first_name": first_name, 
        "last_name": last_name, 
        "username": username, 
        "email": email, 
        "password": hash_password(password),
        "address": {
            "address":"",
            "city": "",
            "suburb":"",
            "state":"",
            "post_code":""
        },
        "logged_in": True, 
        "last_login_date": dt
    }
    return mydict

def create_dict_user(current_user_count, first_name, last_name, username, email, password, dt):
    '''
        Creates and returns a dictionary for user
    '''
    # Creates dictionary of user details and adds it to database
    mydict = create_dict_admin(current_user_count, first_name, last_name, username, email, password, dt)
    mydict['cart'] = []
    mydict['tag_data'] = {}
    mydict['purchase_history'] = []
    mydict['claimed_coupons'] = []
    mydict['claimable_coupons'] = []
    mydict['coupon_timer'] = ""
    mydict['number_of_tags_clicked'] = 0

    return mydict

def registry_check(email, username, password, client_collection):
    '''
        Handles all the error checking when registering
    '''
    if not valid_email(email):
        return {
            'success': False,
            'message': 'Email is invalid.'
        }

    if len(password) < 6:
        return {
            'success': False,
            'message': "Password is too short"
        }

    user_query = check_user_exists(username, client_collection)

    # Checks whether username is unique and sends a 'Fail' if not
    if user_query is not None:
        return {
            'success': False,
            'message': 'Username already in use'
        }
    
    return {
        'success': True,
        'message': 'Passed through registry check'
    }

def get_user_id(token):
    decoded = decode_token(token)
    user_id = decoded['user_id']
    return user_id

def get_user_coupons(token):
    user = get_user_with_token(token, database.users)
    return user['claimed_coupons']

def has_claimable_coupon(token):
    user = get_user_with_token(token, database.users)
    if(len(user['claimable_coupons']) > 0):
        return True
    return False