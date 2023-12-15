# Functions related to the operations of items that can be done by authorized admins
# Actions include:
# - Adding items
# - Removing unsold items
# - Selling items
# - Add product details such as tags, price and description
# - Edit above product details

'''
Format of items dictionary
    'items': [
        {
            'item_id': (#int)
            'admin_id': (#int)
            'item_name': (#string)
            'description': (#string)
            'tags': (#string)
            'price': (#float)
            'stock': (#int)
            'avg_rating': (#float)
            'reviews': (#list)
            'sold': (#int)
            'revenue': (#float)
            'sales_history': [{
                'date': (#string of format %d/%m/%Y)
                'quantity_sold': (#int)
            }]
        }
    ]
'''

#import
try:
    from database import items, admin_tokens, item_counter, all_tags
    from auth import decode_token
except ModuleNotFoundError:
    from .database import items, admin_tokens, item_counter, all_tags
    from .auth import decode_token
import json
from PIL import Image
from scraper import get_image_url
import urllib

def update_tag_collection(tags: list):
    for tag in tags:
        tag_check = all_tags.find_one({'tag': tag})
        if tag_check is None:
            url = ''
            try:
                url = get_image_url(tag)
            except:
                print('failed to get tag image url')
                url = ''
            all_tags.insert_one({'tag': tag, 'tag_id': all_tags.count_documents({}), 'image_url': url})

default_filename = 'default.jpg'

def item_add(token, item_name, desc, tags, price, stock):
    '''
        Adds an item to the website with aforementioned arguments.
        Parameters:
            token (string): token which can be decoded to obtain the id of the admin responsible for adding the item
            item_name (string): name of the string
            desc (string): description of item
            tags (list of strings): tags refering to item
            price (double): price of item
            stock (int): stock of item to be added to sell
            img_url (str): url to image for item
        Return success condition and following message describing the result
    '''
    # Check if valid token given
    if not valid_admin_token(token):
        return {
            'success': False,
            'message': 'User is not recognized in the system as an admin'
        }
    u_id = decode_token(token)['user_id']
    
    # Check that item_name exists
    if len(item_name) == 0:
        return {
            'success': False,
            'message': 'Item name is not given'
        }
    
    # Check if description of item is no longer than 250 characters
    if len(desc) >= 250:
        return {
            'success': False,
            'message': 'Description exceeds 250 characters'
        }
    
    # Check stock given is valid (must be more than zero)
    if stock <= 0:
        return {
            'success': False,
            'message': 'Invalid stock of items to add (Stock to add must be more than zero)'
        }
    
    # Round off the price to 2 decimal places
    round_price = round(price, 2)

    # Get current item count using item_counter db
    if item_counter.find().collection.count_documents({}) == 0:
        # Initialize an item counter
        counter = {'item_counter': 0}
        item_counter.insert_one(counter)
    cursor = item_counter.find_one()
    cur_item_count = cursor['item_counter']

    """
    # Setup figure to show trend of current item sales
    fig = plt.figure(figsize=(10, 10))
    #win = fig10.add_subplot(1,1,1)
    fig = plt.xlabel("Days")
    fig = plt.ylabel("Items sold")
    fig = plt.title("Item sold for .. days")
    """

    # Create the resulting dict to append
    result_dict = {
        'item_id': cur_item_count,
        'admin_id': u_id,
        'item_name': item_name,
        'description': desc,
        'tags': tags,
        'price': round_price,
        'stock': stock,
        'avg_rating': 0,
        'image_url': 'http://127.0.0.1:2434/static/itemphotos/default.jpg',
        'reviews': [],
        'sold': 0,
        'revenue': 0,
        'sales_history': []
    }
    items.insert_one(result_dict)

    # Increments item count
    replace_query = {'item_counter': cur_item_count}
    replace_val = { "$set": {'item_counter':cur_item_count + 1} }
    item_counter.update_one(replace_query, replace_val)
    update_tag_collection(tags)

    return {
        'success': True,
        'message': 'Item has been successfully added',
        'item_id': cur_item_count
    }

def item_add_with_image(token, item_name, desc, tags, price, stock, image_url):
    if not valid_admin_token(token):
        return {
            'success': False,
            'message': 'User is not recognized in the system as an admin'
        }

    if item_counter.find().collection.count_documents({}) == 0:
        # Initialize an item counter
        counter = {'item_counter': 0}
        item_counter.insert_one(counter)
    cursor = item_counter.find_one()
    item_id = cursor['item_counter']

    image_result = attempt_save_item_photo(image_url, item_id)
    if not image_result['success']:
        return image_result
    add_result = item_add(token, item_name, desc, tags, price, stock)
    if not add_result['success']:
        return add_result

    item = items.find_one({'item_id': item_id})
    if item is None:
        return {
            'success': False,
            'message': 'Something went wrong with item creation'
        }

    items.update_one({'item_id': item_id}, {'$set': {'image_url': image_result['image_url']}})

    return {
        'success': True,
        'message': 'Item has been successfully added',
        'item_id': item_id
    }

    

def item_edit_name(token, item_id, new_item_name):
    '''
        Edits and replaces the old item name with the new item name
    '''
    # Checks if item exists in the database and is editable by the admin with admin_username
    if not is_editable(token, item_id):
        return {
            'success': False,
            'message': 'User is not permissible to edit the item'
        }
    
    if new_item_name == "":
        return {
            'success': False,
            'message': 'Item name is not given'
        }

    # replaces old item_name with new one
    u_id = decode_token(token)['user_id']
    replace_query = {'item_id': item_id, 'admin_id': u_id}
    replace_val = { "$set": {'item_name':new_item_name} }
    items.update_one(replace_query, replace_val)
    return {
        'success': True,
        'message': 'Item name has been successfully edited'
    }

def item_edit_desc(token, item_id, new_item_desc):
    '''
        Edits and replaces the old item description with a new item description
    '''
    # Checks if item exists in the database and is editable by the admin with admin_username
    if not is_editable(token, item_id):
        if not valid_admin_token(token):
            return {
                'success': False,
                'message': 'Token is not valid'
            }
        else:
            return {
                'success': False,
                'message': 'User is not permissible to edit the item',
                'admin_id': decode_token(token)['user_id'],
                'item_id': item_id
            }
    
    if len(new_item_desc) >= 250:
        return {
            'success': False,
            'message': 'Description exceeds 250 characters'
        }
    
    # replaces old item description with a new one
    u_id = decode_token(token)['user_id']
    replace_query = {'item_id': item_id, 'admin_id': u_id}
    replace_val = { "$set": {'description':new_item_desc} }
    items.update_one(replace_query, replace_val)
    return {
        'success': True,
        'message': 'Item description has been successfully edited'
    }

def item_edit_tags(token, item_id, new_tags):
    '''
        Replaces all the tags previously with a new list of tags
    '''
    # Checks if item exists in the database and is editable by the admin with admin_username
    if not is_editable(token, item_id):
        return {
            'success': False,
            'message': 'User is not permissible to edit the item'
        }

    # replaces old tags with new tags
    u_id = decode_token(token)['user_id']
    replace_query = {'item_id': item_id, 'admin_id': u_id}
    replace_val = { "$set": {'tags':new_tags} }
    items.update_one(replace_query, replace_val)
    update_tag_collection(new_tags)
    return {
        'success': True,
        'message': 'Item tags have been successfully edited'
    }

def item_edit_price(token, item_id, new_price):
    '''
        Replaces past item price with a new price
    '''
    # Checks if item exists in the database and is editable by the admin with admin_username
    if not is_editable(token, item_id):
        return {
            'success': False,
            'message': 'User is not permissible to edit the item'
        }
    
    # replaces old tags with new tags
    u_id = decode_token(token)['user_id']
    replace_query = {'item_id': item_id, 'admin_id': u_id}
    replace_val = { "$set": {'price':new_price} }
    items.update_one(replace_query, replace_val)
    return {
        'success': True,
        'message': 'Price of item have been successfully edited'
    }

def item_edit_stock(token, item_id, new_stock):
    '''
        Edits the stock an item that is already added, the admin
        can either add or decrease a stock.
    '''
    # Checks if item exists in the database and is editable by the admin with admin_username
    if not is_editable(token, item_id):
        return {
            'success': False,
            'message': 'User is not permissible to edit the item'
        }
    
    # Check if new_stock is valid
    if new_stock < 0:
        return {
            'success': False,
            'message': 'Invalid stock of items (Stocks must be equal to or greater than zero)'
        }

    # replaces old stock with new stock
    u_id = decode_token(token)['user_id']
    replace_query = {'item_id': item_id, 'admin_id': u_id}
    replace_val = { "$set": {'stock':new_stock} }
    items.update_one(replace_query, replace_val)
    return {
        'success': True,
        'message': 'Item stocks have been successfully edited'
    }

def item_remove(token, item_id):
    '''
        Removes item with the corresponding item_id from the database by an assigned admin
        Parameters:
            token (string): token of authentication
            item_id (string): id of item to edit description
        Return success condition and following message describing the result
    '''
    # Checks if item exists in the database and is editable by the admin with admin_username
    if not is_editable(token, item_id):
        return {
            'success': False,
            'message': 'User is not permissible to remove the item'
        }
    
    # Removes item from the database
    u_id = decode_token(token)['user_id']
    delete_query = {'$and': [{"item_id": item_id}, {"admin_id": u_id}] }
    items.delete_one(delete_query)
    return {
        'success': True,
        'message': 'Item has been successfully removed'
    }

def item_sell(item_id, amount_to_sell):
    '''
        Sells an item in the website
        Parameters:
            item_id (int): id of item being sold
            amount_sold (int): amount of items to sell
        Return success condition and following message describing the result
    '''
    # Find the item with the item_id in the database of items
    item_query = {"item_id": item_id}
    item_found = items.find_one(item_query)
    if item_found is None:  # item does not exist
        return {
            'success': False,
            'message': 'Item does not exist in the database'
        }
    
    # Get the number of stocks of item to sell and check if there is enough stock
    remaining_stock = item_found['stock']
    if (amount_to_sell > remaining_stock):
        return {
            'success': False,
            'message': 'There is not enough stock of items remaining for you to buy'
        }
    
    # Enough stock, updates stock
    new_stock = remaining_stock - amount_to_sell
    replace_query = {'item_id': item_id}
    replace_val = { "$set": {'stock':new_stock} }
    items.update_one(replace_query, replace_val)

    #  Then sell and pay the admin
    return {
        'success': True,
        'message': 'Item has been succesfully sold'
    }


def item_get_details(token, item_id):
    if not valid_admin_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }

    # Find the item that is given by the item_id
    item_query = {"item_id": int(item_id)}
    item = items.find_one(item_query)
    if item is None:  # item does not exist
        return {
            'success': False,
            'message': 'Item does not exist in the database'
        }

    item_details = {
        'item_id': item['item_id'],
        'admin_id': item['admin_id'],
        'item_name': item['item_name'],
        'description': item['description'],
        'tags': item['tags'],
        'price': item['price'],
        'stock': item['stock'],
        'image_url': item['image_url'],
        'sold': item['sold'],
        'revenue': item['revenue']
    }

    # Return
    return {
        'success': True,
        'details': item_details
    }

def item_get_detailsUser(token, item_id):
    # if not valid_admin_token(token):
    #     return {
    #         'success': False,
    #         'message': 'User does not exist.'
    #     }

    # Find the item that is given by the item_id
    item_query = {"item_id": int(item_id)}
    item = items.find_one(item_query)
    if item is None:  # item does not exist
        return {
            'success': False,
            'message': 'Item does not exist in the database'
        }

    item_details = {
        'item_id': item['item_id'],
        'admin_id': item['admin_id'],
        'item_name': item['item_name'],
        'description': item['description'],
        'tags': item['tags'],
        'price': item['price'],
        'stock': item['stock'],
        'image_url': item['image_url']
    }

    # Return
    return {
        'success': True,
        'details': item_details
    }

def get_admin_items(token):
    if not valid_admin_token(token):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    
    u_id = decode_token(token)['user_id']
    items_query = {"admin_id": u_id}
    item_list = items.find(items_query)

    result_list = []
    for item in item_list:
        result_dict = {
            'item_id': item['item_id'],
            'admin_id': item['admin_id'],
            'item_name': item['item_name'],
            'description': item['description'],
            'tags': item['tags'],
            'price': item['price'],
            'stock': item['stock'],
            'sold': item['sold']
        }
        result_list.append(result_dict)

    return {
        'success': True,
        'details': json.dumps(result_list)
    }

def item_get_sales_history(token, item_id):
    '''
        Returns a list of sales with their appropriate dates for a specified item_id
        This can only be called by the admins
    '''
    if not valid_admin_token(token):
        return {
            'success': False,
            'message': 'Admin does not exist.'
        }

    # Find the item that is given by the item_id
    item_query = {"item_id": int(item_id)}
    item = items.find_one(item_query)
    if item is None:  # item does not exist
        return {
            'success': False,
            'message': 'Item does not exist in the database'
        }

    # Return
    return {
        'success': True,
        'details': json.dumps(item['sales_history'])
    }

def admin_get_sales_history(token):
    '''
        Returns a list of sales of all items added / associated with the admin from the token given
        Will return a list of items revenue to their dates.
    '''
    if not valid_admin_token(token):
        return {
            'success': False,
            'message': 'Admin does not exist.'
        }

    # Get the total sales for all items
    u_id = decode_token(token)['user_id']
    total_sales = []
    """
    Total sales is a list of dictionary of form:
        [{
            'date': (string of format %d/%m/%Y)
            'revenue': (#float)
        }]
    """

    for item in items.find():
        if item['admin_id'] == u_id:
            # Only add sales of items added by the admin
            for sale in item['sales_history']:
                cur_date = sale['date']
                i = find_list_dict_index(total_sales, 'date', cur_date)

                if i != -1: # Entry of date already exist, Add total revenue
                    total_rev = total_sales[i]['revenue'] + sale['quantity_sold'] * item['price']
                    total_sales[i]['revenue'] = total_rev
                else:
                    new_sale = {
                        'date': cur_date,
                        'revenue': sale['quantity_sold'] * item['price']
                    }
                    total_sales.append(new_sale)

    # Return
    return {
        'success': True,
        'details': json.dumps(total_sales)
    }

'''
    Helper functions
'''
def valid_admin_token(token):
    '''
        Checks if token given is valid and exists in the system currently
        Token should point to an existing admin
    '''
    token_filter = {"token": token}
    id_query = admin_tokens.find(token_filter)

    if id_query.collection.count_documents({}) == 0:
        return False
    
    # An instance of user id found, return True
    return True

def is_editable(token, item_id):
    '''
        Checks if an item is editable, i.e.
        the item with the corresponding item_id must have been added
        by the admin with the same admin_username
    '''
    if not valid_admin_token(token):
        return False

    u_id = decode_token(token)['user_id']
    query_check = {'$and': [{"item_id": item_id}, {"admin_id": u_id}] }
    valid_query = items.find_one(query_check)

    if valid_query is None:
        return False
    
    # An instance of item added by the admin found, return false
    return True

def find_list_dict_index(lst, key, value):
    """
    Helper function to return the index
    of a specified key with a specified value in a list of dict
    Parameters:
        lst: list of dicts (of any kind)
        key: key-pair of the dict
        value: value you are loooking for in the dict ket
    Return -1 if index is not fount and index i if there is key-value pair in the list of dicts
    """
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def upload_item_photo(token, img_url, item_id):
    if not valid_admin_token(token):
        return {
            'success': False,
            'message': 'Invalid Token'
        }

    save_result = attempt_save_item_photo(img_url, item_id)
    if not save_result['success']:
        return save_result

    item = items.find_one({'item_id': item_id})
    if item is None:
        return {
            'success': False,
            'message': 'Item does not exist'
        }

    items.update_one({'item_id': item_id}, {'$set': {'image_url': save_result['image_url']}})
    return save_result

def attempt_save_item_photo(img_url, item_id):
    try:
        req = urllib.request.urlopen(img_url)
        http_status = req.getcode()

        if http_status != 200:
            return {
                'success': False,
                'message': 'Bad Image URL'
            }

        img = Image.open(req)

        if img.format != 'JPEG':
            return {
                'success': False,
                'message': 'Image not in JPEG format'
            }

        path = 'static/itemphotos/' + str(item_id) + '.jpg'
        image_url = 'http://127.0.0.1:2434/' + path
        img.save(path)

        return {
            'success': True,
            'image_url': image_url
        }
    except:
        return {
                'success': False,
                'message': 'Failed to save photo'
            }

def add_sales_history(date, item_id, count):
    """
    Add a sales history directly for testing purposes
    Parameters:
        date: (string of format %d/%m/%Y)
        item_id: id of item
        count: number of items to add to sales history (#int)
    """
    item_query = {"item_id": item_id}
    item_found = items.find_one(item_query)

    # update the total revenue for the item given the amount of items bought and its current price
    current_revenue = item_found['price'] * count
    total_revenue = item_found['revenue'] + current_revenue
    replace_val = { "$set": {'revenue': total_revenue} }
    items.update_one(item_query, replace_val)

    # Get current date and update sales history
    cur_history = item_found['sales_history']
    date_exist = False
    for sale in cur_history:
        if sale['date'] == date: # There is already a instance of item sold for that date
            sale['quantity_sold'] = sale['quantity_sold'] + count
            date_exist = True

    if date_exist is False: # There has yet to be any item sold for the item for the current date
        new_sale = {
            'date': date,
            'quantity_sold': count
        }
        cur_history.append(new_sale)
    # Update database
    replace_val = { "$set": {'sales_history': cur_history} }
    items.update_one(item_query, replace_val)