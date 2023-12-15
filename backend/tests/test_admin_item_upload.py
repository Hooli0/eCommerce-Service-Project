import auth
import database
import admin_items
import json

def test_add_image_success():
    database.clear_database()

    admin1 = auth.auth_register_admin("Main", "Admin", "MainAdmin", "a@a.com", "password", database.admins, database.admin_tokens)
    assert admin1['success']

    image_result = admin_items.item_add_with_image(admin1['token'], "desk from IKEA", "", ['Furniture'], 19.389, 3, 
                                                'https://www.ikea.com/au/en/images/products/arkelstorp-desk__0735967_PE740301_S5.JPG')
    assert image_result['success']

    item_check = admin_items.item_get_details(admin1['token'], 0)
    assert item_check['success']
    item_details = json.loads(item_check['details'])
    assert item_details['item_name'] == 'desk from IKEA'
    assert item_details['item_id'] == 0
    database.clear_database()

def test_add_image_failure():
    database.clear_database()

    admin1 = auth.auth_register_admin("Main", "Admin", "MainAdmin", "a@a.com", "password", database.admins, database.admin_tokens)
    assert admin1['success']

    image_result = admin_items.item_add_with_image(admin1['token'], "desk from IKEA", "", ['Furniture'], 19.389, 3, 'this aint no link')
    assert not image_result['success']

    item_check = admin_items.item_get_details(admin1['token'], 0)
    assert not item_check['success']

    database.clear_database()

def test_add_image_success_item_fail():
    database.clear_database()

    admin1 = auth.auth_register_admin("Main", "Admin", "MainAdmin", "a@a.com", "password", database.admins, database.admin_tokens)
    assert admin1['success']

    image_result = admin_items.item_add_with_image(admin1['token'], "", "", ['Furniture'], 19.389, 3, 
                                                        'https://www.ikea.com/au/en/images/products/arkelstorp-desk__0735967_PE740301_S5.JPG')
    assert not image_result['success']

    item_check = admin_items.item_get_details(admin1['token'], 0)
    assert not item_check['success']

    database.clear_database()