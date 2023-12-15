'''
    Coupon related functions
'''
from datetime import datetime, timedelta
import auth
import database

time_interval_1 = timedelta(seconds=5)
time_interval_2 = timedelta(seconds=10)

#time_interval_1 = timedelta(minutes=1)
#time_interval_2 = timedelta(minutes=2)

def get_coupon_timer(token):
    '''
        Returns the coupon timer The returned timer is always gonna be below 24 hours
    '''
    if not auth.check_token_exists(token, database.user_tokens):
        return {
            'success': False,
            'message': 'User is not logged in.'
        }

    user = auth.get_user_with_token(token, database.users)

    remaining_time = (str_to_datetime(user['coupon_timer']) + time_interval_1) - datetime.now()

    return{
        'success': True,
        'coupon_timer': str(remaining_time.total_seconds())
    }

def check_for_daily_coupon_reward(token):
    user = auth.get_user_with_token(token, database.users)
    if(user['coupon_timer'] == ""):
        database.users.update_one({"username": user['username']}, {"$set": {"coupon_timer": datetime_to_str(datetime.now())}})
        return {
            'success': True,
            'message': "Coupon timer has been started for the first time"
        }
    
    if(datetime.now() >= str_to_datetime(user['coupon_timer']) + time_interval_1 and datetime.now() <= str_to_datetime(user['coupon_timer']) + time_interval_2):
        add_claimable_coupon_to_user(token, 0.1)
        database.users.update_one({"username": user['username']}, {"$set": {"coupon_timer": datetime_to_str(datetime.now())}})
        return {
            'success': True,
            'message': "Coupon timer has been reset for next daily reward"
        }
    elif(datetime.now() > str_to_datetime(user['coupon_timer']) + time_interval_2):
        database.users.update_one({"username": user['username']}, {"$set": {"coupon_timer": datetime_to_str(datetime.now())}})
        return {
            'success': True,
            'message': "You have failed to login daily"
        }
    else:
        return {
            'success': False,
            'message': "You have not met the requirements for receiving a daily login. Come back later"
        }

def check_for_coupon_expiry(token):
    user = auth.get_user_with_token(token, database.users)
    claimable_coupons = user['claimable_coupons'].copy()
    index  = 0
    for coupon in user['claimable_coupons']:
        if(str_to_datetime(coupon['expiry_date']) <= datetime.now()):
            claimable_coupons.pop(index)
    database.users.update_one({"username": user['username']}, {"$set": {"claimable_coupons": claimable_coupons}})

def claim_coupons(token):
    '''
        Claims all coupon that are claimable
    '''
    check_for_coupon_expiry(token)
    user = auth.get_user_with_token(token, database.users)
    claimable_coupons = user['claimable_coupons'].copy()
    claimed_coupons = user['claimed_coupons'].copy()

    for coupon in user['claimable_coupons']:
        claimable_coupons.pop(0)
        coupon['id'] = len(claimed_coupons)
        claimed_coupons.append(coupon)

    if len(claimed_coupons) > len(user['claimed_coupons']) and len(claimable_coupons) < len(user['claimable_coupons']):
        database.users.update_one({"username": user['username']}, {"$set": {"claimed_coupons": claimed_coupons}})
        database.users.update_one({"username": user['username']}, {"$set": {"claimable_coupons": claimable_coupons}})
        return {
            'success': True,
            'message': "User claimed coupon(s)"
        }
    else:
        return {
            'success': False,
            'message': "There were no coupons to be claimed or coupons have expired"
        }

def add_claimable_coupon_to_user(token, discount_value):
    '''
        Create a coupon
    '''
    coupon = {
        'discount_value': discount_value,
        'expiry_date': datetime_to_str(datetime.now() + time_interval_1),
        'id': -1
    }
    user = auth.get_user_with_token(token, database.users)
    lst = user['claimable_coupons'].copy()
    lst.append(coupon)
    database.users.update_one({"username": user['username']}, {"$set": {"claimable_coupons": lst}})

def apply_coupons(original_price, coupon_list):
    '''
        Applies the discount
    '''
    discounted_price = original_price
    for coupon in coupon_list:
        discounted_price = discounted_price * (1.0 - coupon['discount_value'])

    return discounted_price

def process_used_coupons(token, coupon_list):
    user = auth.get_user_with_token(token, database.users)
    lst = []
    for coupon in user['claimed_coupons']:
        if not find_same_coupon_id(coupon['id'], coupon_list):
            lst.append(coupon)

    if not len(lst) == 0:
        reset_coupon_ids(lst)

    database.users.update_one({"username": user['username']}, {"$set": {"claimed_coupons": lst}})

    return {
        'success': True,
        'message': "Used coupons have been processed"
    }

'''
    Helper functions
'''

def str_to_datetime(string : str):
    '''
        Converts a string to datetime
    '''
    return datetime.strptime(str(string), "%Y-%m-%d, %H:%M:%S")

def datetime_to_str(date_time : datetime):
    '''
        Converts a datetime to string
    '''
    return date_time.strftime("%Y-%m-%d, %H:%M:%S")

def find_same_coupon_id(id, lst):
    for coupon in lst:
        if(coupon['id'] == id):
            return True
    return False

def reset_coupon_ids(lst):
    index = 0
    for coupon in lst:
        lst[index]['id'] = index
        index += 1
    return lst

def has_claimable_coupon(token):
    user = auth.get_user_with_token(token, database.users)
    if(len(user['claimable_coupons']) > 0):
        return True
    return False