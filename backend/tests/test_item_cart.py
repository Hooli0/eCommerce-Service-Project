from backend import item_cart, admin_items, auth
from backend.database import clear_database, users, user_tokens, users, admin_tokens, admins
import pymongo
import json

def test_item_cart_add_inval_token():
    clear_database()
    # Try passing an invalid token (admin token)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert admin_tokens.find().collection.count_documents({}) == 1
    assert user_tokens.find().collection.count_documents({}) == 0
    
    # Add valid item
    result = admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    assert result['success'] is True
    # Fail as we try to add item to cart using admin account
    result = item_cart.item_cart_add(id["token"], 0, 1)
    assert result['success'] is False
    assert result['message'] == 'User does not exist.'

def test_item_cart_add_inval_item_id():
    clear_database()
    # Try passing an invalid item_id
    id = auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    assert user_tokens.find().collection.count_documents({}) == 1
    assert admin_tokens.find().collection.count_documents({}) == 0

    # Fail as we try to pass inexistent item_id
    result = item_cart.item_cart_add(id["token"], 0, 1)
    assert result['success'] is False
    assert result['message'] == 'Item does not exist in the database'

def test_item_cart_add_inval_item_amount():
    clear_database()
    # Try passing an invalid item_amount
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert admin_tokens.find().collection.count_documents({}) == 1
    assert user_tokens.find().collection.count_documents({}) == 0
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    assert user_tokens.find().collection.count_documents({}) == 1
    assert admin_tokens.find().collection.count_documents({}) == 1

    # Fail as we try to pass inval item_amount
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    assert result['success'] is True

    result = item_cart.item_cart_add(id2["token"], 0, 0)
    assert result['success'] is False
    assert result['message'] ==  'Invalid amount of item to add to cart.'

    result = item_cart.item_cart_add(id2["token"], 0, 100)
    assert result['success'] is False
    assert result['message'] ==  'The admin of the item does not have enough stock for you to add to the cart'

def test_item_cart_add_success():
    clear_database()
    # Try passing valid case
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    assert users.find().collection.count_documents({}) == 1

    # Check when valid case passed
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    assert result['success'] is True

    result = item_cart.item_cart_add(id2["token"], 0, 2)
    assert result['success'] is True
    assert result['message'] ==  'Item has been successfully added to the cart'

    # Check if cart in user database is updated
    assert users.find().collection.count_documents({}) == 1
    result = users.find_one()
    result['first_name'] == "Waterson"
    result['last_name'] == "Rex"
    len(result['cart']) == 1
    result['cart'][0]['count'] == 2
    result['cart'][0]['item']['stock'] == 3

def test_item_cart_add_same_item():
    clear_database()
    # Try passing valid case
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    assert users.find().collection.count_documents({}) == 1

    # Check when valid case passed
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = item_cart.item_cart_add(id2["token"], 0, 2)
    assert result['success'] is True
    assert result['message'] ==  'Item has been successfully added to the cart'

    # Check when trying to add same item
    result = item_cart.item_cart_add(id2["token"], 0, 1)
    assert result['success'] is False
    assert result['message'] ==  'Wrong function to call. Call item_cart_set_count instead'

def test_item_cart_add_multiple_items():
    clear_database()
    # Try passing valid case
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    id3 = auth.auth_register_user("Linda", "Jones", "LinJones", "user2@emailthing.com", "password", users, user_tokens)
    assert users.find().collection.count_documents({}) == 2

    # Check when valid case passed
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = item_cart.item_cart_add(id2["token"], 0, 2)
    assert result['success'] is True
    assert result['message'] ==  'Item has been successfully added to the cart'

    # Check when valid case passed
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = item_cart.item_cart_add(id3["token"], 0, 3)
    assert result['success'] is True
    assert result['message'] ==  'Item has been successfully added to the cart'

    # Check if cart in user database is updated
    assert users.find().collection.count_documents({}) == 2
    result = users.find_one({"first_name": "Waterson"})
    result['first_name'] == "Waterson"
    result['last_name'] == "Rex"
    len(result['cart']) == 1
    result['cart'][0]['count'] == 2
    result['cart'][0]['item']['stock'] == 3

    # Check if cart for other user database is updated
    assert users.find().collection.count_documents({}) == 2
    result = users.find_one({"first_name": "Linda"})
    result['first_name'] == "Linda"
    result['last_name'] == "Jones"
    len(result['cart']) == 1
    result['cart'][0]['count'] == 3
    result['cart'][0]['item']['stock'] == 3

def test_item_cart_set_count_inval_token():
    clear_database()
    # Try passing an invalid token (admin token)
    id = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    
    # Add valid item
    result = admin_items.item_add(id['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    assert result['success'] is True
    # Fail as we try to add item to cart using admin account
    result = item_cart.item_cart_set_count(id["token"], 0, 3)
    assert result['success'] is False
    assert result['message'] == 'User does not exist.'

def test_item_cart_set_count_inval_item_id():
    clear_database()
    # Try passing an invalid item_id
    id = auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)

    # Fail as we try to pass inexistent item_id
    result = item_cart.item_cart_set_count(id["token"], 0, 1)
    assert result['success'] is False
    assert result['message'] == 'Item does not exist in the database'

def test_item_cart_set_count_inval_item_cart():
    clear_database()
    # Try passing an invalid item_id
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)

    # Fail as we try to pass inexistent item in cart
    result = item_cart.item_cart_set_count(id2["token"], 0, 1)
    assert result['success'] is False
    assert result['message'] == 'Item does not exist in the cart'

def test_item_cart_increment_count_inval_count():
    clear_database()
    # Checks
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)

    # add item to cart
    result = item_cart.item_cart_add(id2['token'], 0, 3)
    assert result['success'] is True
    # Set count but fail as stock is 3 limited
    result = item_cart.item_cart_set_count(id2["token"], 0, 4)
    assert result['success'] is False
    assert result['message'] == 'The admin of the item does not have enough stock for you to add more items to the cart'

    result = item_cart.item_cart_set_count(id2['token'], 0, 0)
    assert result['success'] is False
    assert result['message'] == 'Cannot decrease the count of the item to equal to or less than zero'

def test_item_cart_set_count_valid():
    clear_database()
    # Checks
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)

    # add item to cart
    result = item_cart.item_cart_add(id2['token'], 0, 2)
    assert result['success'] is True
    result = users.find_one({"first_name": "Waterson"})
    result['cart'][0]['count'] == 2

    # Increment count and succeed
    result = item_cart.item_cart_set_count(id2["token"], 0, 3)
    assert result['success'] is True
    assert result['message'] == 'Item count has been successfully updated'
    result = users.find_one({"first_name": "Waterson"})
    result['first_name'] == "Waterson"
    result['last_name'] == "Rex"
    len(result['cart']) == 1
    result['cart'][0]['count'] == 3
    result['cart'][0]['item']['stock'] == 3

def test_item_cart_remove_item_valid():
    clear_database()
    # Checks
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_add(id1['token'], "IKEA lamp", "", ['furniture', 'IKEA'], 30.36, 2)

    # add item to cart
    result = item_cart.item_cart_add(id2['token'], 0, 2)
    assert result['success'] is True
    result = item_cart.item_cart_add(id2['token'], 1, 2)
    assert result['success'] is True

    # Check
    result = users.find_one({"first_name": "Waterson"})
    len(result['cart']) == 2
    result['cart'][0]['count'] == 2
    result['cart'][1]['count'] == 2

    # Remove and check
    result = item_cart.item_cart_remove_item(id2["token"], 0)
    assert result['success'] is True
    assert result['message'] == 'Item has been successfully removed from the cart'
    result = users.find_one({"first_name": "Waterson"})
    len(result['cart']) == 1
    result['cart'][0]['count'] == 2
    result['cart'][0]['item']['item_id'] == 1
    result['cart'][0]['item']['item_name'] == "IKEA lamp"

def test_item_get_total_price_valid():
    clear_database()
    # Checks
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_add(id1['token'], "IKEA lamp", "", ['furniture', 'IKEA'], 30.36, 2)

    # add item to cart
    result = item_cart.item_cart_add(id2['token'], 0, 2)
    assert result['success'] is True
    result = item_cart.item_cart_add(id2['token'], 1, 2)
    assert result['success'] is True

    # Check
    result = users.find_one({"first_name": "Waterson"})
    len(result['cart']) == 2
    result['cart'][0]['count'] == 2
    result['cart'][1]['count'] == 2

    # Get total price and check
    result = item_cart.item_cart_get_total_price(id2["token"], [])
    assert round(result['original_price'],2) == 99.50
    assert round(result['discounted_price'],2) == 99.50

def test_item_get_total_price_valid_with_coupon():
    clear_database()
    # Checks
    id1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    id2 = auth.auth_register_user("Waterson", "Rex", "RexWaterson", "user@emailthing.com", "password", users, user_tokens)
    result = admin_items.item_add(id1['token'], "IKEA desk", "", ['furniture', 'IKEA'], 19.389, 3)
    result = admin_items.item_add(id1['token'], "IKEA lamp", "", ['furniture', 'IKEA'], 30.36, 2)

    # add item to cart
    result = item_cart.item_cart_add(id2['token'], 0, 2)
    assert result['success'] is True
    result = item_cart.item_cart_add(id2['token'], 1, 2)
    assert result['success'] is True

    # Check
    result = users.find_one({"first_name": "Waterson"})
    len(result['cart']) == 2
    result['cart'][0]['count'] == 2
    result['cart'][1]['count'] == 2

    # Get total price and check
    result = item_cart.item_cart_get_total_price(id2["token"], [{"discount_value":0.1}])
    assert round(result['original_price'],2) == 99.50
    assert round(result['discounted_price'],2) == round(99.50 * 0.9, 2)