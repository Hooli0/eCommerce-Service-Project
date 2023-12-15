import json
import auth
import recommendations
import admin_items
import database
from server import admin_login
import spoofer
import search
import requests
import checkout
from scraper import get_image_url

def get_paypal_access_token(client_id, secret):
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

def test_order_create(token):
    url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [
                {
                "amount": {
                    "currency_code": "USD",
                    "value": "100.00"
                }
            }
        ],
        "application_context": {
            "return_url": "http://www.google.com"
        }
    }

    oauth_response = requests.post(url,
                                headers= {'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + str(token) },
                                json=order_data)
    
    # Get OAuth JSON in response body
    oauth_body_json = oauth_response.json()
    return oauth_body_json

def capture_order(token, order_id):
    url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders/' + str(order_id) + '/capture'

    data = {}

    oauth_response = requests.post(url,
                                headers= {'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + str(token) },
                                json=data)
    
    # Get OAuth JSON in response body
    oauth_body_json = oauth_response.json()
    return oauth_body_json

if __name__ == '__main__':
    spoofer.spoof_data()

    #paypal_token = str(get_paypal_access_token("AQZ-7RjcZnP7eZd2uQRn1fz72c12elxAYxVCCogH_CTE6JypzQ0GwUoF9RJvchumHq82bVYJwWVaOEYF", 
    #"EL-LzeVq9xh1FErIzFY-eWIdWXcEgPIzfNxrZyAUj9rGdYyEQFGVEcArT435KOIJlwmB0Gse_YyCl6Dl"))

    #print(paypal_token)
    #print("--------------------------- TOKEN ABOVE ---------------------------")
    #print(str(test_order_create(paypal_token)))
    #print(capture_order("A21AAK9DbZLs0kyxu9UsJgtM7ddlpIIJEBJt5sA0Os2ZBxoUO5upf8t1u-BFCyAYgneDq5AFbhKfLSkgmNCgkAcxmrVAsfKIA", "9UW821889S475030P"))
    #admin_login_result = auth.auth_login("MainAdmin", "password", database.admins, database.admin_tokens)
    #login_result = auth.auth_login("User1", "password", database.users, database.user_tokens)
    #recommendations.record_user_clicked_item(login_result["token"], 0)
    #print(str(recommendations.generate_recs_for_user(login_result["token"], 5)))

    print(search.get_all_tags()['tags'])

    #admin_items.upload_item_photo(admin_login_result['token'], 'https://fthmb.tqn.com/0omM8mKUKJO2uqWvNvC9MvleHDI=/2000x2000/filters:fill(auto,1)/IKEA-Micke-computer-desk-5a2a2323beba330037ac19c7.jpg', 0)
    #print(admin_items.item_get_detailsUser(login_result['token'], 0))

    #database.clear_database()
    #user_vector = numpy.array([2, 2, 0])
    #item_vector = numpy.array([1, 0, 1])
    #dot = numpy.dot(user_vector, item_vector)
    #magnitudes = numpy.linalg.norm(user_vector) * numpy.linalg.norm(item_vector)

    #print(dot/magnitudes)


    