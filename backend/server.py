import json
import sys
from flask import Flask, request
from flask_cors import CORS
from json import dumps
import auth
import admin_items
import item_cart
import recommendations
import spoofer
import search
import checkout
import item_ratings
import share
import coupon
from database import admins, admin_tokens, users, user_tokens, items

app = Flask(__name__, static_url_path='/static')
CORS(app)


@app.route('/admin/register', methods=['POST'])
def admin_register():
    payload = request.get_json()
    first_name = payload["first_name"]
    last_name = payload["last_name"]
    username = payload["username"]
    email = payload["email"]
    password = payload["password"]

    return dumps(auth.auth_register_admin(first_name, last_name, username, email, password, admins, admin_tokens))

@app.route('/admin/login', methods=['POST'])
def admin_login():
    payload = request.get_json()
    username = payload["username"]
    password = payload["password"]

    return dumps(auth.auth_login(username, password, admins, admin_tokens))

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    payload = request.get_json()
    # username = payload["username"]
    token = payload["token"]

    return dumps(auth.auth_logout(token, admins, admin_tokens))

@app.route('/admin/details', methods=['GET'])
def admin_get_details():
    # payload = request.get_json()
    # token = payload["token"]
    token = request.args.get('token')

    return dumps(auth.get_admin_details(token, admins, admin_tokens))

@app.route('/admin/check_token', methods=['GET'])
def admin_check_token_validity():
    # payload = request.get_json()
    # token = payload["token"]
    token =  request.args.get('token')

    return dumps(auth.check_token_exists(token, admin_tokens))

@app.route('/admin/change_username', methods=['POST'])
def admin_change_username():
    payload = request.get_json()
    new_username = payload["new_username"]
    token = payload["token"]

    return dumps(auth.change_username(new_username, token, admins, admin_tokens))

@app.route('/admin/change_password', methods=['POST'])
def admin_change_password():
    payload = request.get_json()
    new_password = payload["new_password"]
    token = payload["token"]

    return dumps(auth.change_password(new_password, token, admins, admin_tokens))

######################## user-related routes ##############################################
@app.route('/user/register', methods=['POST'])
def user_register():
    payload = request.get_json()
    first_name = payload["first_name"]
    last_name = payload["last_name"]
    username = payload["username"]
    email = payload["email"]
    password = payload["password"]

    return dumps(auth.auth_register_user(first_name, last_name, username, email, password, users, user_tokens))

@app.route('/user/login', methods=['POST'])
def user_login():
    payload = request.get_json()
    username = payload["username"]
    password = payload["password"]

    login_result = auth.auth_login(username, password, users, user_tokens)
    if(login_result['success']):
        coupon.check_for_daily_coupon_reward(login_result['token'])
        coupon.check_for_coupon_expiry(login_result['token'])
    return dumps(login_result)

@app.route('/user/logout', methods=['POST'])
def user_logout():
    payload = request.get_json()
    # username = payload["username"]
    token = payload["token"]

    return dumps(auth.auth_logout(token, users, user_tokens))

@app.route('/user/details', methods=['GET'])
def user_get_details():
    # payload = request.get_json()
    # token = payload["token"]
    token = request.args.get('token')

    return dumps(auth.get_user_details(token, users, user_tokens))

@app.route('/user/check_token', methods=['GET'])
def user_check_token_validity():
    # payload = request.get_json()
    # token = payload["token"]
    token = request.args.get('token')

    return dumps(auth.check_token_exists(token, user_tokens))

@app.route('/user/change_username', methods=['POST'])
def user_change_username():
    payload = request.get_json()
    new_username = payload["new_username"]
    token = payload["token"]

    return dumps(auth.change_username(new_username, token, users, user_tokens))

@app.route('/user/change_password', methods=['POST'])
def user_change_password():
    payload = request.get_json()
    new_password = payload["new_password"]
    token = payload["token"]

    return dumps(auth.change_password(new_password, token, users, user_tokens))

@app.route('/user/change_address', methods=['POST'])
def user_change_address():
    payload = request.get_json()
    address = payload["address"]
    city = payload["city"]
    suburb = payload["suburb"]
    state = payload["state"]
    post_code = payload["post_code"]
    token = payload["token"]

    return dumps(auth.change_address(address, city, suburb, state, post_code, token, users, user_tokens))

######################## admin-items interaction http functions ############################

@app.route('/admin/item/add', methods=['POST'])
def admin_add_items():
    payload = request.get_json()
    token = payload["token"]
    item_name = payload["item_name"]
    desc = payload["description"]
    tags = payload["tags"]
    price = payload["price"]
    stock = payload["stock"]
    image_url = payload['image_url']

    return dumps(admin_items.item_add_with_image(token, item_name, desc, tags, price, stock, image_url))

@app.route('/admin/item/edit/name', methods=['PUT'])
def admin_edit_item_name():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]
    new_name = payload["item_name"]

    return dumps(admin_items.item_edit_name(token, item_id, new_name))

@app.route('/admin/item/edit/desc', methods=['PUT'])
def admin_edit_item_desc():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]
    new_desc = payload["description"]

    return dumps(admin_items.item_edit_desc(token, item_id, new_desc))

@app.route('/admin/item/edit/tags', methods=['PUT'])
def admin_edit_item_tags():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]
    new_tags = payload["tags"]

    return dumps(admin_items.item_edit_tags(token, item_id, new_tags))

@app.route('/admin/item/edit/price', methods=['PUT'])
def admin_edit_item_price():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]
    new_price = payload["price"]

    return dumps(admin_items.item_edit_price(token, item_id, new_price))

@app.route('/admin/item/edit/stock', methods=['PUT'])
def admin_edit_item_stock():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]
    new_stock = payload["stock"]

    return dumps(admin_items.item_edit_stock(token, item_id, new_stock))

@app.route('/admin/item/remove', methods=['DELETE'])
def admin_remove_item():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]

    return dumps(admin_items.item_remove(token, item_id))

@app.route('/admin/item/sell', methods=['PUT'])
def admin_sell_item():
    payload = request.get_json()
    item_id = payload["item_id"]
    item_sold = payload["amount_sold"]

    return dumps(admin_items.item_sell(item_id, item_sold))

@app.route('/admin/item/details', methods=['GET'])
def get_item_details():
    # payload = request.get_json()
    # token = payload['token']
    # item_id = payload['item_id']
    token =  request.args.get('token')
    item_id =  request.args.get('item_id')

    return dumps(admin_items.item_get_details(token, item_id))

@app.route('/user/item/details', methods=['GET'])
def item_get_detailsUser():
    # payload = request.get_json()
    # token = payload['token']
    # item_id = payload['item_id']
    token =  request.args.get('token')
    item_id =  request.args.get('item_id')

    return dumps(admin_items.item_get_detailsUser(token, item_id))

@app.route('/admin/items', methods=['GET'])
def get_items_admin():
    # payload = request.get_json()
    # token = payload['token']
    token = request.args.get("token")

    return dumps(admin_items.get_admin_items(token))

@app.route('/admin/item/sales/history', methods=['GET'])
def get_item_sales_history():
    token = request.args.get("token")
    item_id =  request.args.get('item_id')

    return dumps(admin_items.item_get_sales_history(token, item_id))

@app.route('/admin/sales/history', methods=['GET'])
def get_admin_sales_history():
    token = request.args.get("token")

    return dumps(admin_items.admin_get_sales_history(token))

'''
    Returns a list of item ids related to a given item
    Payload should contain:
        item_id (int): the id of the item to use as a base
        number_of_recs (int): the maximum number of recommendations to return
    Returns:
        success (bool): whether the operation was successful or not
        item_ids (list of int): the item ids of the related items found
'''
@app.route('/recommendations/from_item', methods=['GET'])
def get_recs_from_item():
    # payload = request.get_json()
    # item_id = payload["item_id"]
    # number_of_recs = payload["number_of_recs"]
    item_id =  request.args.get('item_id')
    number_of_recs =  request.args.get('number_of_recs')

    return dumps(recommendations.generate_recs_from_item(item_id, number_of_recs))

'''
    Returns a list of item ids that are recommended for a user
    Payload should contain:
        token (int): token corresponding to the user to display recommendations for
        number_of_recs (int): the maximum number of recommendations to return
    Returns:
        success (bool): whether the operation was successful or not
        item_ids (list of int): the item ids of the related items found
'''
@app.route('/recommendations/from_user', methods=['GET'])
def get_recs_from_user():
    # payload = request.get_json()
    # token = payload["token"]
    # number_of_recs = payload["number_of_recs"]
    token =  request.args.get('token')
    number_of_recs =  request.args.get('number_of_recs')
    return dumps(recommendations.generate_recs_for_user(token, number_of_recs))

'''
    Used to create or reset the spoof data used for testing
'''
@app.route('/test/reset', methods=['POST'])
def reset_spoof_data():
    return dumps(spoofer.spoof_data())

'''
    Records the user clicking on a certain item so that recommendations can be updated
    Payload should contain:
        token (int): token corresponding to the user who clicked on the item
        item_id (int): the id of the item that was clicked on
    Returns:
        success (bool): whether the operation was successful or not
'''
@app.route('/recommendations/record_click', methods=['PUT'])
def record_user_click():
    payload = request.get_json()
    item_id = payload["item_id"]
    token = payload["token"]

    return dumps(recommendations.record_user_clicked_item(token, item_id))


######################## item-carts related routes ##############################################

@app.route('/item/getCart', methods=['GET'] )
def get_user_cart():
    token =  request.args.get('token')
    return dumps(item_cart.get_user_cart(token))

@app.route('/item/cart/add', methods=['POST'])
def add_item_to_cart():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]
    amount = payload["amount"]

    return dumps(item_cart.item_cart_add(token, item_id, amount))

@app.route('/item/cart/set/count', methods=['PUT'])
def set_cart_item_count():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]
    amount = payload["new_count"]

    return dumps(item_cart.item_cart_set_count(token, item_id, amount))

@app.route('/item/cart/remove/item', methods=['DELETE'])
def remove_cart_item():
    payload = request.get_json()
    token = payload["token"]
    item_id = payload["item_id"]

    return dumps(item_cart.item_cart_remove_item(token, item_id))

@app.route('/item/cart/get/totalprice', methods=['GET'])
def get_cart_item_total_price():
    token = request.args.get('token')
    coupon_list = json.loads(request.args.get('coupon_list'))

    return dumps(item_cart.item_cart_get_total_price(token, coupon_list))

@app.route('/item/cart/get/itemcount', methods=['GET'])
def get_cart_item_item_count():
    # payload = request.get_json()
    # token = payload["token"]
    token = request.args.get('token')

    return dumps(item_cart.item_cart_get_item_count(token))

@app.route('/item/cart/get/totalcount', methods=['GET'])
def get_cart_item_total_count():
    token = request.args.get('token')

    return dumps(item_cart.item_cart_get_total_items_count(token))

@app.route('/item/cart/checkout', methods=['GET'])
def get_cart_item_checkout():
    token = request.args.get('token')

    return dumps(item_cart.item_cart_checkout(token))

'''
    Returns all tags in the item database
    Args should contain:
        token (str): token corresponding to a user
    Returns:
        success (bool): whether the operation was successful or not
        tags (list of str): all tags on the database
'''

@app.route('/all_tags', methods=['GET'])
def all_tags():
    token = request.args.get("token")

    if auth.check_token_exists(token, user_tokens) is False:
        return dumps({
            'success': False,
            'message': 'User is not logged in.'
        })

    return dumps(search.get_all_tags())

'''
    Returns items with names matching a text search
    Args should contain:
        token (str): token corresponding to a user
        string (str): the string used for the search
    Returns:
        success (bool): whether the operation was successful or not
        items (list of dict): items resulting from the search
'''

@app.route('/search/user_general', methods=['GET'])
def general_search():
    search_string = request.args.get("string")
    token = request.args.get("token")

    if auth.check_token_exists(token, user_tokens) is False:
        return dumps({
            'success': False,
            'message': 'User is not logged in.'
        })

    return dumps(search.search_item(search_string))

'''
    Returns all items containing a certain tag
    Args should contain:
        token (str): token corresponding to a user
        tag (str): the tag to search for
    Returns:
        success (bool): whether the operation was successful or not
        items (list of dict): the items containing the input tag
'''

@app.route('/search/tag', methods=['GET'])
def get_items_with_tag():
    tag = request.args.get("tag")
    token = request.args.get("token")

    if auth.check_token_exists(token, user_tokens) is False:
        return dumps({
            'success': False,
            'message': 'User is not logged in.'
        })

    return dumps(search.get_items_with_tag(tag))

'''
    Immediately checkout a single item
    Payload should contain:
        token (str): token corresponding to a user
        item_id (int): id of item to buy
        return_url (str): url that paypal will redirect to after checkout
    On success, returns:
        success (bool): whether the operation was successful or not
        order_id (str): the id of the order, to use for capturing after checkout
        redirect_url (str): link to paypal which will initiate the checkout process
'''

@app.route('/checkout/buy_now', methods=['POST'])
def checkout_buy_now():
    payload = request.get_json()
    item_id = payload["item_id"]
    token = payload["token"]
    return_url = payload['return_url']

    if auth.check_token_exists(token, user_tokens) is False:
        return dumps({
            'success': False,
            'message': 'User is not logged in.'
        })

    return dumps(checkout.checkout_item(item_id, return_url))

'''
    Checkout a user's cart
    Payload should contain:
        token (str): token corresponding to a user
        return_url (str): url that paypal will redirect to after checkout
    On success, returns:
        success (bool): whether the operation was successful or not
        order_id (str): the id of the order, to use for capturing after checkout
        redirect_url (str): link to paypal which will initiate the checkout process
        receipt (dict): contains information about the purchase
    Receipt contains (each should be self explanatory):
        'list of items bought' (list of dict)
        'total unique items purchased' (int)
        'total count of items purchased' (int)
        'total cost' (float)
'''

@app.route('/checkout/cart', methods=['POST'])
def checkout_cart():
    payload = request.get_json()
    token = payload["token"]
    return_url = payload['return_url']
    original_price = payload['original_price']
    discounted_price = payload['discounted_price']
    used_coupons = payload['used_coupons']

    result = checkout.item_cart_checkout(token, return_url, original_price, discounted_price)

    if(result['success']):
        coupon.process_used_coupons(token, used_coupons)

    return dumps(result)

'''
    Captures payment after approval by user
    Payload should contain:
        token (str): token corresponding to a user
        order_id (str): order to capture payment for
    Returns:
        success (bool): whether the operation was successful or not
'''

@app.route('/checkout/capture', methods=['POST'])
def checkout_capture():
    payload = request.get_json()
    order_id = payload["order_id"]
    token = payload["token"]

    if auth.check_token_exists(token, user_tokens) is False:
        return dumps({
            'success': False,
            'message': 'User is not logged in.'
        })

    return dumps(checkout.capture_order(token, order_id))

'''
    Create a review for an item
    Payload should contain:
        token (int): token corresponding to a user
        item_id (int): id of item to review
        rating (int): user's rating of item out of 5 (but can technically be anything)
        review (str): user's written review of item
    Returns:
        success (bool): whether the review was successfully created or not
'''
@app.route('/item/create_review', methods=['POST'])
def create_review():
    payload = request.get_json()
    item_id = payload["item_id"]
    rating = payload['rating']
    review = payload['review']
    token = payload["token"]

    if auth.check_token_exists(token, user_tokens) is False:
        return dumps({
            'success': False,
            'message': 'User is not logged in.'
        })

    return dumps(item_ratings.create_review(token, item_id, rating, review))

'''
    Get reviews for item
    Args should contain:
        token (str): token corresponding to a user
        item_id (int): id of item to get reviews of
    Returns:
        success (bool): whether the review was successfully created or not
        reviews (list): list of review data
        avg_rating (int): the average rating of the item
'''
@app.route('/item/get_reviews', methods=['GET'])
def get_reviews():
    item_id = request.args.get("item_id")
    token = request.args.get("token")

    if auth.check_token_exists(token, user_tokens) is False:
        return dumps({
            'success': False,
            'message': 'User is not logged in.'
        })

    return dumps(item_ratings.get_reviews_for_item(item_id))
    
'''
    Returns the purchase history of a given user
    Args should contain:
        token (str): token corresponding to a user
    Returns:
        success (bool): whether the operation was successful or not
        history (list of dictionary): the user's purchase history
    Each history dict contains:
        date (string): date of purchase
        items (list of item): items purchased
'''

@app.route('/user/history', methods=['GET'])
def get_purchase_history():
    token = request.args.get("token")
    return dumps(checkout.get_purchase_history(token))


@app.route('/user/coupon_timer', methods=['GET'])
def get_coupon_timer():
    token = request.args.get("token")
    return dumps(coupon.get_coupon_timer(token))

@app.route('/user/claim_coupons', methods=['POST'])
def claim_coupons():
    payload = request.get_json()
    token = payload['token']
    return dumps(coupon.claim_coupons(token))

@app.route('/user/check_for_daily_reward', methods=['POST'])
def check_for_daily_coupon_reward():    
    payload = request.get_json()
    token = payload['token']
    return dumps(coupon.check_for_daily_coupon_reward(token))

'''
    Update the image of a given item
    Payload should contain:
        token (str): token corresponding to an admin
        item_id (int): id of item to update image
        image_url (str): url to image for item
    Returns:
        success (bool): whether the operation was successful or not
        image_url (str): the url to the image on the server
'''
@app.route('/item/upload_image', methods=['PUT'])
def upload_item_image():
    payload = request.get_json()
    item_id = payload["item_id"]
    token = payload["token"]
    image_url = payload['image_url']

    return dumps(admin_items.upload_item_photo(token, image_url, item_id))

@app.route('/share/item_cart', methods=['POST'])
def get_same_items_from_cart():
    payload = request.get_json()
    token = payload["token"]
    user_id = payload["user_id"]
    cart_id = payload['cart_id']
    return dumps(share.get_same_items_from_cart(token, user_id, cart_id))

@app.route('/user/user_id', methods=['GET'])
def get_user_id():
    token = request.args.get("token")
    return dumps(auth.get_user_id(token))

@app.route('/user/coupons', methods=['GET'])
def get_user_coupons():
    token = request.args.get("token")
    return dumps(auth.get_user_coupons(token))

@app.route('/user/has_claimable_coupon', methods=['GET'])
def has_claimable_coupon():
    token = request.args.get("token")
    return dumps(coupon.has_claimable_coupon(token))

if __name__ == "__main__":
    '''
    admins.delete_many({})
    admin_tokens.delete_many({})
    users.delete_many({})
    items.delete_many({})
    '''
    app.debug = True
    app.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 2434))
