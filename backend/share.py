'''
    A file containing all related functions to social media sharing
'''
import auth
import item_cart
import database
import item_cart

def get_same_items_from_cart(token, user_id: int, cart_id: int):
    auth.check_token_exists(token, database.user_tokens)
    user_id_query = database.users.find_one({"user_id": int(user_id)})
    selected_purchase_history = user_id_query['purchase_history'][cart_id]
    item_list = selected_purchase_history['items']
    result_dict = item_cart.item_cart_add_list(token, item_list)
    result_dict['item_list'] = item_list
    return result_dict

