import auth
import database
import requests
import item_cart
from datetime import date
# from matplotlib import pyplot as plt

client_id = "AQZ-7RjcZnP7eZd2uQRn1fz72c12elxAYxVCCogH_CTE6JypzQ0GwUoF9RJvchumHq82bVYJwWVaOEYF"
secret = "EL-LzeVq9xh1FErIzFY-eWIdWXcEgPIzfNxrZyAUj9rGdYyEQFGVEcArT435KOIJlwmB0Gse_YyCl6Dl"

def get_paypal_access_token():
    url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    oauth_response = requests.post(url,
                                headers= {'Accept': 'application/json',
                                            'Accept-Language': 'en_US'},
                                auth=(client_id, secret),
                                data={'grant_type': 'client_credentials'})
    
    # Get OAuth JSON in response body
    oauth_body_json = oauth_response.json()
    # Get access token
    return oauth_body_json['access_token']


def execute_paypal_order(amount: float, return_url: str):
    paypal_token = get_paypal_access_token()

    url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [
                {
                "amount": {
                    "currency_code": "AUD",
                    "value": str(amount)
                }
            }
        ],
        "application_context": {
            "return_url": str(return_url)
        }
    }

    oauth_response = requests.post(url,
                                headers= {'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + str(paypal_token)},
                                json=order_data)
    
    return oauth_response.json()

def checkout_item(token: str, item_id: int, return_url: str):
    if not auth.check_token_exists(token, database.user_tokens):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = auth.decode_token(token)['user_id']
    user_query = {"user_id": u_id}
    user = database.users.find_one(user_query)
    item_data = database.items.find_one({"item_id": int(item_id)})
    if item_data is None:
        return {
            'success': False,
            'message': 'Item not found'
        }
    
    del item_data['_id']
    response = execute_paypal_order(item_data['price'], return_url)

    if(response['status'] == 'CREATED'):
        links = response['links']
        approve_link_data = links[1]
        update_purchase_history(u_id, user['purchase_history'], [item_data])
        return {
            'success': True,
            'order_id': response['id'],
            'redirect_url': approve_link_data['href']
        }
    else:
        return {
            'success': False,
            'message': 'Paypal error'
        }

def capture_order(token: str, order_id: str):
    url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders/' + str(order_id) + '/capture'

    data = {}
    u_id = auth.decode_token(token)['user_id']
    user_query = {"user_id": u_id}
    user = database.users.find_one(user_query)
    cur_cart = user['cart']

    for cart_item in cur_cart:
        # Reduce the stock of the items in the database as they will be sold to the user
        item_query = {"item_id": cart_item['item']['item_id']}
        item_found = database.items.find_one(item_query)
        cur_stock = item_found['stock']
        replace_val = { "$set": {'stock': max(cur_stock - cart_item['count'], 0)} }
        database.items.update_one(item_query, replace_val)

        # update amount of item sold for admins to view
        new_sold = item_found['sold'] + cart_item['count']
        replace_val = { "$set": {'sold': new_sold} }
        database.items.update_one(item_query, replace_val)

        # update the total revenue for the item given the amount of items bought and its current price
        current_revenue = item_found['price'] * cart_item['count']
        total_revenue = item_found['revenue'] + current_revenue
        replace_val = { "$set": {'revenue': total_revenue} }
        database.items.update_one(item_query, replace_val)

        # Get current date and update sales history
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
        database.items.update_one(item_query, replace_val)
        

    # Clear the current shopping cart
    cur_cart.clear()
    replace_query = {'user_id': u_id}
    replace_val = { "$set": {'cart':cur_cart} }
    database.users.update_one(replace_query, replace_val)

    paypal_token = get_paypal_access_token()
    oauth_response = requests.post(url,
                                headers= {'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + str(paypal_token) },
                                json=data)
    
    # Get OAuth JSON in response body
    response = oauth_response.json()
    if(response['status'] == 'COMPLETED'):
        return {
            'success': True
        }
    else:
        return {
            'success': False,
            'message': 'Paypal error'
        }

def item_cart_checkout(token: str, return_url: str, original_price, total_cost):
    '''
        Checkout / purchases all the items in the current user's cart
        Parameters:
            token (string): unique identifier for user
        Return a receipt upon success.
        Note that doing a checkout means that a receipt will be generated and the shopping cart will be emptied
        in the process.
    '''
    if not auth.check_token_exists(token, database.user_tokens):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = auth.decode_token(token)['user_id']
    user_query = {"user_id": u_id}
    user = database.users.find_one(user_query)
    cur_cart = user['cart']
    receipt = {
        'list of items bought': [],
        'total unique items purchased': item_cart.item_cart_get_item_count(token),
        'total count of items purchased': item_cart.item_cart_get_total_items_count(token),
        'original_price': original_price,
        'total cost': total_cost
    }

    for cart_item in cur_cart:
        del cart_item['item']['_id']
        receipt['list of items bought'].append(cart_item['item'])

    # Do the payment
    response = execute_paypal_order(total_cost, return_url)

    if(response['status'] == 'CREATED'):
        links = response['links']
        approve_link_data = links[1]
        update_purchase_history(u_id, user['purchase_history'], cur_cart)
        return {
            'success': True,
            'order_id': response['id'],
            'redirect_url': approve_link_data['href'],
            'details': receipt
        }
    else:
        return {
            'success': False,
            'message': 'Paypal error'
        }

def update_purchase_history(user_id: int, purchase_history: list, items: list):
    today = str(date.today())

    ob = {
        "date": today,
        "items": items,
        "cart_id": len(purchase_history)
    }

    purchase_history.append(ob)
    database.users.update_one({"user_id": user_id}, {"$set": {"purchase_history": purchase_history}})

def get_purchase_history(token: str):
    if not auth.check_token_exists(token, database.user_tokens):
        return {
            'success': False,
            'message': 'User does not exist.'
        }
    u_id = auth.decode_token(token)['user_id']
    user_query = {"user_id": u_id}
    user = database.users.find_one(user_query)

    return {
        'success': True,
        'history': user['purchase_history']
    }
