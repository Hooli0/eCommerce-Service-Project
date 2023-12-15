from backend import admin_items, auth
from backend.database import clear_database, admin_tokens, admins, items
import pymongo
import json
from datetime import date

def test_item_add_inval_token():
    clear_database()
    # Try passing an invalid token (invalid token after logging out)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert admin_tokens.find().collection.count_documents({}) == 1
    auth.auth_logout(id['token'], admins, admin_tokens)
    assert admin_tokens.find().collection.count_documents({}) == 0
    
    # fail as not recognized / invalid token
    result = admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    assert result['success'] is False
    assert result['message'] == 'User is not recognized in the system as an admin'

def test_item_add_inval_name():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    # fail as no name is given
    result = admin_items.item_add(id['token'], "", "Top quality IKEA desk", ['furniture', 'IKEA'], 19.389, 3)
    assert result['success'] is False
    assert result['message'] == 'Item name is not given'

def test_item_add_inval_desc():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    # fail as description is too long
    desc = ''
    for x in range (0, 250):
        desc += "A"
    result = admin_items.item_add(id['token'], "IKEA cupboard", desc, ['furniture', 'IKEA'], 19.389, 3)
    assert result['success'] is False
    assert result['message'] == 'Description exceeds 250 characters'

def test_item_add_inval_stock():
    clear_database()
    # Fail as stock set is 0 initially
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    result = admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 0)
    assert result['success'] is False
    assert result['message'] == 'Invalid stock of items to add (Stock to add must be more than zero)'

def test_item_add_valid():
    clear_database()
    # register admin
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    result = admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    assert result['success'] is True
    assert result['message'] == 'Item has been successfully added'

    # Add first item
    result = admin_items.item_get_details(id['token'], 0)
    obj = json.loads(result['details'])
    assert obj['item_id'] == 0
    assert obj['admin_id'] == 0 
    assert obj['item_name'] == "IKEA desk"
    assert obj['description'] == ""
    assert obj['tags'] == ['furniture', 'IKEA']
    assert obj['price'] == 19.39
    assert obj['stock'] == 3

    # Add second item
    admin_items.item_add(id['token'], "IKEA lamp", "", ['furniture', 'IKEA'], 20, 1)
    result = admin_items.item_get_details(id['token'], 1)
    obj = json.loads(result['details'])
    assert obj['item_id'] == 1
    assert obj['admin_id'] == 0 
    assert obj['item_name'] == "IKEA lamp"
    assert obj['description'] == ""
    assert obj['tags'] == ['furniture', 'IKEA']
    assert obj['price'] == 20.00
    assert obj['stock'] == 1

def test_item_edit_name_invalid():
    clear_database()
    # Try passing an invalid token (invalid token after logging out)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    auth.auth_logout(id['token'], admins, admin_tokens)

    # Should be uneditable as token is not valid
    result = admin_items.item_edit_name(id['token'], 0, "Wooden desk")
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

    # uneditable as invalid name
    auth.auth_login("BobJones", "password", admins, admin_tokens)
    result = admin_items.item_edit_name(id['token'], 0, "")
    assert result['success'] is False
    assert result['message'] == 'Item name is not given'

    # Passing an invalid item_id
    result = admin_items.item_edit_name(id['token'], 11, "Wooden desk")
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

def test_edit_name_valid():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_edit_name(id['token'], 0, "Wooden desk")
    assert result['success'] is True
    assert result['message'] == 'Item name has been successfully edited'

    # detail check
    result = admin_items.item_get_details(id['token'], 0)
    obj = json.loads(result['details'])
    assert obj['item_id'] == 0
    assert obj['admin_id'] == 0 
    assert obj['item_name'] == "Wooden desk"
    assert obj['description'] == ""
    assert obj['tags'] == ['furniture', 'IKEA']
    assert obj['price'] == 19.39
    assert obj['stock'] == 3

def test_item_edit_desc_invalid():
    clear_database()
    # Try passing an invalid token (invalid token after logging out)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    auth.auth_logout(id['token'], admins, admin_tokens)

    # Should be uneditable as token is not valid
    result = admin_items.item_edit_desc(id['token'], 0, "Comfortable wooden desk")
    assert result['success'] is False
    assert result['message'] == 'Token is not valid'

    # uneditable as invalid desc
    auth.auth_login("BobJones", "password", admins, admin_tokens)
    desc = ''
    for x in range (0, 250):
        desc += "A"
    result = admin_items.item_edit_desc(id['token'], 0, desc)
    assert result['success'] is False
    assert result['message'] == 'Description exceeds 250 characters'

    # Passing an invalid item_id
    result = admin_items.item_edit_desc(id['token'], 1, "Wooden desk")
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

def test_edit_desc_valid():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_edit_desc(id['token'], 0, "Wooden desk")
    assert result['success'] is True
    assert result['message'] == 'Item description has been successfully edited'

    # detail check
    result = admin_items.item_get_details(id['token'], 0)
    obj = json.loads(result['details'])
    assert obj['item_id'] == 0
    assert obj['admin_id'] == 0 
    assert obj['item_name'] == "IKEA desk"
    assert obj['description'] == "Wooden desk"
    assert obj['tags'] == ['furniture', 'IKEA']
    assert obj['price'] == 19.39
    assert obj['stock'] == 3

def test_item_edit_tags_invalid():
    clear_database()
    # Try passing an invalid token (invalid token after logging out)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    auth.auth_logout(id['token'], admins, admin_tokens)

    # Should be uneditable as token is not valid
    result = admin_items.item_edit_tags(id['token'], 0, "Comfortable wooden desk")
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

    # Passing an invalid item_id
    auth.auth_login("BobJones", "password", admins, admin_tokens)
    result = admin_items.item_edit_tags(id['token'], 420, "Wooden desk")
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

def test_edit_tags_valid():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_edit_tags(id['token'], 0, ['furniture', 'household', 'luxury'])
    assert result['success'] is True
    assert result['message'] == 'Item tags have been successfully edited'

    # detail check
    result = admin_items.item_get_details(id['token'], 0)
    obj = json.loads(result['details'])
    assert obj['item_id'] == 0
    assert obj['admin_id'] == 0 
    assert obj['item_name'] == "IKEA desk"
    assert obj['description'] == ""
    assert obj['tags'] == ['furniture', 'household', 'luxury']
    assert obj['price'] == 19.39
    assert obj['stock'] == 3

def test_item_edit_price_invalid():
    clear_database()
    # Try passing an invalid token (invalid token after logging out)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    auth.auth_logout(id['token'], admins, admin_tokens)

    # Should be uneditable as token is not valid
    result = admin_items.item_edit_price(id['token'], 0, 88.00)
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

    # Passing an invalid item_id
    auth.auth_login("BobJones", "password", admins, admin_tokens)
    result = admin_items.item_edit_price(id['token'], 110, 88.00)
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

def test_edit_price_valid():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_edit_price(id['token'], 0, 69.420)
    assert result['success'] is True
    assert result['message'] == 'Price of item have been successfully edited'

    # detail check
    result = admin_items.item_get_details(id['token'], 0)
    obj = json.loads(result['details'])
    assert obj['item_id'] == 0
    assert obj['admin_id'] == 0 
    assert obj['item_name'] == "IKEA desk"
    assert obj['description'] == ""
    assert obj['tags'] == ['furniture', 'IKEA']
    assert obj['price'] == 69.42
    assert obj['stock'] == 3

def test_item_edit_stock_invalid():
    clear_database()
    # Try passing an invalid token (invalid token after logging out)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    auth.auth_logout(id['token'], admins, admin_tokens)

    # Should be uneditable as token is not valid
    result = admin_items.item_edit_stock(id['token'], 0, 12)
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

    # uneditable as invalid stock
    auth.auth_login("BobJones", "password", admins, admin_tokens)
    result = admin_items.item_edit_stock(id['token'], 0, -1)
    assert result['success'] is False
    assert result['message'] == 'Invalid stock of items (Stocks must be equal to or greater than zero)'

    # Passing an invalid item_id
    result = admin_items.item_edit_stock(id['token'], 12, 1)
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to edit the item'

def test_edit_stock_valid():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_edit_stock(id['token'], 0, 0)
    assert result['success'] is True
    assert result['message'] == 'Item stocks have been successfully edited'

    # detail check
    result = admin_items.item_get_details(id['token'], 0)
    obj = json.loads(result['details'])
    assert obj['item_id'] == 0
    assert obj['admin_id'] == 0 
    assert obj['item_name'] == "IKEA desk"
    assert obj['description'] == ""
    assert obj['tags'] == ['furniture', 'IKEA']
    assert obj['price'] == 19.39
    assert obj['stock'] == 0

def test_item_remove_invalid():
    clear_database()
    # Try passing an invalid token (invalid token after logging out)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    auth.auth_logout(id['token'], admins, admin_tokens)

    # Should be uneditable as token is not valid
    result = admin_items.item_remove(id['token'], 0)
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to remove the item'

    # uneditable as invalid item_id
    auth.auth_login("BobJones", "password", admins, admin_tokens)
    result = admin_items.item_remove(id['token'], 12)
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to remove the item'

    # uneditable as it was a different admin who added the item
    id2 = auth.auth_register_admin("James", "Orlean", "JamesOrlean", "james@emailthing.com", "password2", admins, admin_tokens)    
    result = admin_items.item_remove(id2['token'], 0)
    assert result['success'] is False
    assert result['message'] == 'User is not permissible to remove the item'

    result = admin_items.get_admin_items(id2['token'])
    assert result['success'] is True
    obj = json.loads(result['details'])
    assert obj == []

def test_item_remove_valid():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_remove(id['token'], 0)
    assert result['success'] is True
    assert result['message'] == 'Item has been successfully removed'

    # detail check
    result = admin_items.item_get_details(id['token'], 0)
    assert result['success'] is False
    assert result['message'] == 'Item does not exist in the database'

def test_item_get_sales_history():
    clear_database()
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    result = admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 10)
    assert result['success'] is True

    # empty sales history before bought
    result = admin_items.item_get_sales_history(id['token'], 0)
    assert result['success'] is True
    obj = json.loads(result['details'])
    assert len(obj) == 0

    # Check admin sales history
    result = admin_items.admin_get_sales_history(id['token'])
    assert result['success'] is True
    obj = json.loads(result['details'])
    assert len(obj) == 0

    # Buy 2 instance and check sales history
    item_found = items.find_one({"item_id": 0})
    first_purchase = {
        'item': item_found,
        'count': 2
    }
    update_sales_history(first_purchase)
    result = admin_items.item_get_sales_history(id['token'], 0)
    assert result['success'] is True
    obj = json.loads(result['details'])
    assert len(obj) == 1
    assert obj[0]['date'] == (date.today()).strftime("%d/%m/%Y")
    assert obj[0]['quantity_sold'] == 2

    result = admin_items.admin_get_sales_history(id['token'])
    assert result['success'] is True
    obj = json.loads(result['details'])
    assert len(obj) == 1
    assert obj[0]['date'] == (date.today()).strftime("%d/%m/%Y")
    assert obj[0]['revenue'] == 38.78

    # Second purchase with diff count and still same day. Confirm sales history is accurate
    second_purchase = {
        'item': item_found,
        'count': 4
    }
    update_sales_history(second_purchase)
    result = admin_items.item_get_sales_history(id['token'], 0)
    assert result['success'] is True
    obj = json.loads(result['details'])
    assert len(obj) == 1
    assert obj[0]['date'] == (date.today()).strftime("%d/%m/%Y")
    assert obj[0]['quantity_sold'] == 6

    result = admin_items.admin_get_sales_history(id['token'])
    assert result['success'] is True
    obj = json.loads(result['details'])
    assert len(obj) == 1
    assert obj[0]['date'] == (date.today()).strftime("%d/%m/%Y")
    assert obj[0]['revenue'] == 116.34

def update_sales_history(cart_item):
    """
        Helper function to confirm this part is working
    """
    # Get current date and update sales history
    item_query = {"item_id": cart_item['item']['item_id']}
    item_found = items.find_one(item_query)
    today = (date.today()).strftime("%d/%m/%Y")
    cur_history = item_found['sales_history']
    date_exist = False
    for sale in cur_history:
        if sale['date'] == today: # There is already a instance of item sold for that date
            sale['quantity_sold'] = sale['quantity_sold'] + cart_item['count']
            date_exist = True

    if date_exist is False: # There has yet to be any item sold for the item for the current date
        new_sale = {
            'date': today,
            'quantity_sold': cart_item['count']
        }
        cur_history.append(new_sale)
    # Update database
    replace_val = { "$set": {'sales_history': cur_history} }
    items.update_one(item_query, replace_val)