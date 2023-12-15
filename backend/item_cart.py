# Functions related to the operations of shopping carts for the users to use.
# Actions include:
# - Adding items to cart
# - Removing items from cart
# - Purchase items from cart

'''
Format of 'cart' dictionary for each user (refer to cart in auth.py)
    'cart': [{
        'item': (#ITEM dictionary, refer to admin_items.py)
        'count': (#int)
    }]
'''

#import
try:
    from database import items, users, user_tokens
    from auth import decode_token
except ModuleNotFoundError:    
    from .database import items, users, user_tokens
    from .auth import decode_token
import json

from admin_items import item_add
from auth import check_token_exists
import coupon

def get_user_cart(token):
    '''
        Get the total count of items added to the cart
        Parameters:
            token (string): unique identifier for user
        Return total count of items in the cart
    '''
    if not valid_user_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = decode_token(token)['user_id']
    user_query = {"user_id": u_id}
    user = users.find_one(user_query)
    cur_cart = user['cart']
    # print(cur_cart)
    for item in cur_cart:
        print(item)
        print(item['item'])
        print(item['item']['_id'])
        del item['item']['_id']
    return {
        'cart': cur_cart
    }

def item_cart_add(token, item_id, amount):
    '''
        Adds a item that is currently sold in the site to a specified user's cart.
        Parameters:
            token (string): unique identifier for user
            item_id (int): unique identifier for an item
            amount (int): amount of said item to add in the cart (cannot exceed item stock)
        Return success condition and following message describing the result
        Note: will only add item to the cart iff item does not yet exist in the user's cart
    '''
    # Check token validity
    if not valid_user_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = decode_token(token)['user_id']
    
    # Find the item with the item_id in the database
    item_query = {"item_id": item_id}
    item_found = items.find_one(item_query)
    if item_found is None:  # item does not exist
        return {
            'success': False,
            'message': 'Item does not exist in the database'
        }
    
    # Check amount given validity
    amount = int(amount)
    if amount <= 0:
        return {
            'success': False,
            'message': 'Invalid amount of item to add to cart.'
        }
    if amount > item_found['stock']:
        return {
            'success': False,
            'message': 'The admin of the item does not have enough stock for you to add to the cart'
        }

    # Get current user's shopping cart
    user_query = {"user_id": u_id}
    user = users.find_one(user_query)
    cur_cart = user['cart']
    
    # Add item to the cart only if item is not in the cart yet
    cart_item_exist = False
    for cart_item in cur_cart:
        if cart_item['item']['item_id'] == item_found['item_id']:
            cart_item_exist = True
    if cart_item_exist:
        return {
            'success': False,
            'message': 'Wrong function to call. Call item_cart_set_count instead'
        }
    result_cart_item_details = {
        'item': item_found,
        'count': amount
    }
    cur_cart.append(result_cart_item_details)
    
    # Update cart details for user in the database
    replace_query = {'user_id': u_id}
    replace_val = { "$set": {'cart':cur_cart} }
    users.update_one(replace_query, replace_val)
    return {
        'success': True,
        'message': 'Item has been successfully added to the cart'
    }

def item_cart_set_count(token, item_id, new_count):
    '''
        Sets the count of a specified item in the specified user's cart to a new_count.
        Parameters:
            token (string): unique identifier for user
            item_id (int): unique identifier for an item
            new_count (int): new count to be set
        Return success condition and following message describing the result
    '''
    # Check token validity
    if not valid_user_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = decode_token(token)['user_id']
    
    # Find the item with the item_id in the database
    item_query = {"item_id": item_id}
    item_found = items.find_one(item_query)
    if item_found is None:  # item does not exist
        return {
            'success': False,
            'message': 'Item does not exist in the database'
        }
    
    # Find item in the cart of the user
    user_query = {"user_id": u_id}
    user = users.find_one(user_query)
    cur_cart = user['cart']
    cart_item_exist = False
    index = 0
    counter = 0

    for cart_item in cur_cart:
        if cart_item['item']['item_id'] == item_found['item_id']:
            cart_item_exist = True
            index = counter
        counter += 1
    if not cart_item_exist:
        return {
            'success': False,
            'message': 'Item does not exist in the cart'
        }
    
    # Update count iff count do not get to zero and below OR count does not exceed current stock of item
    if new_count <= 0 :
        return {
            'success': False,
            'message': 'Cannot decrease the count of the item to equal to or less than zero'
        }
    elif new_count > item_found['stock']:
        return {
            'success': False,
            'message': 'The admin of the item does not have enough stock for you to add more items to the cart'
        }
    
    # Update and success
    cur_cart[index]['count'] = new_count
    replace_query = {'user_id': u_id}
    replace_val = { "$set": {'cart':cur_cart} }
    users.update_one(replace_query, replace_val)
    return {
        'success': True,
        'message': 'Item count has been successfully updated'
    }

def item_cart_remove_item(token, item_id):
    '''
        Remove the specified item from the specified user's cart.
        Parameters:
            token (string): unique identifier for user
            item_id (int): unique identifier for an item
        Return success condition and following message describing the result
    '''
    # Check token validity
    if not valid_user_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = decode_token(token)['user_id']
    
    # Find the item with the item_id in the database
    item_query = {"item_id": item_id}
    item_found = items.find_one(item_query)
    if item_found is None:  # item does not exist
        return {
            'success': False,
            'message': 'Item does not exist in the database'
        }
    
    # Find item in the cart of the user
    user_query = {"user_id": u_id}
    user = users.find_one(user_query)
    cur_cart = user['cart']
    cart_item_exist = False
    index = 0
    counter = 0

    for cart_item in cur_cart:
        if cart_item['item']['item_id'] == item_found['item_id']:
            cart_item_exist = True
            index = counter
        counter += 1
    if not cart_item_exist:
        return {
            'success': False,
            'message': 'Item does not exist in the cart'
        }

    # Remove item from cart and success
    cur_cart.pop(index)
    replace_query = {'user_id': u_id}
    replace_val = { "$set": {'cart':cur_cart} }
    users.update_one(replace_query, replace_val)
    return {
        'success': True,
        'message': 'Item has been successfully removed from the cart'
    }

def item_cart_get_total_price(token, coupon_list):
    '''
        Get the total price of a current user's cart.
        Parameters:
            token (string): unique identifier for user
        Return total price of the cart (#float)
    ''' 
    # Check token validity
    if not valid_user_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = decode_token(token)['user_id']
    user_query = {"user_id": u_id}
    user = users.find_one(user_query)
    cur_cart = user['cart']

    # Sum all prices of items in the cart
    original_price = 0
    for cart_item in cur_cart:
        original_price += (cart_item['item']['price'] * cart_item['count'])

    discounted_price = coupon.apply_coupons(original_price, coupon_list)

    return {
        "original_price": original_price,
        "discounted_price": discounted_price
    }

def item_cart_get_item_count(token):
    '''
        Get the total amount of items in the current shopping cart
        Parameters:
            token (string): unique identifier for user
        Return total number of unique items in the cart
    ''' 
    if not valid_user_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = decode_token(token)['user_id']
    user_query = {"user_id": u_id}
    user = users.find_one(user_query)
    cur_cart = user['cart']
    return len(cur_cart)

def item_cart_get_total_items_count(token):
    '''
        Get the total count of items added to the cart
        Parameters:
            token (string): unique identifier for user
        Return total count of items in the cart
    '''
    if not valid_user_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = decode_token(token)['user_id']
    user_query = {"user_id": u_id}
    user = users.find_one(user_query)
    cur_cart = user['cart']

    sum = 0
    for cart_item in cur_cart:
        sum += cart_item['count']
    return sum

def item_cart_add_list(token, item_list):
    '''
        Adds the list of items to the current shopping cart
    '''
    if not check_token_exists(token, user_tokens):
        return {
            'success': False,
            'message': "Token not valid"
        }
    all_items_added = True
    for item in item_list:
        query = item_cart_add(token, item['item']['item_id'], item['count'])
        if not query['success']:
            all_items_added = False

    if all_items_added:
        return {
            'success': True,
            'message': "All items were added to the cart"
        }
    else:
        return {
            'success': True,
            'message': "Not all items were added to the cart"
        }

'''
    Helper functions
'''
def valid_user_token(token):
    '''
        Checks if token given is valid and exists in the system currently
        Token should point to an existing user (not admin)
    '''
    token_filter = {"token": token}
    id_query = user_tokens.find(token_filter)

    if id_query.collection.count_documents({}) == 0:
        return False
    
    # An instance of user id found, return True
    return True

def update_item_details(token):
    '''
        Updates the cart details (attributes of cart dictionary)
        Parameters:
            token (string): unique identifier for user
        Return success condition and following message describing the result
    '''
