from datetime import datetime, timedelta
from auth import decode_token, generate_token, get_user_with_token, hash_password
from backend import auth
from backend import coupon
import json
from datetime import datetime
from database import clear_database, myclient, mydb, admins, admin_tokens, users, user_tokens

def test_coupon_timer():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    result = coupon.check_for_daily_coupon_reward(token)
    assert result['success']
    result = coupon.check_for_daily_coupon_reward(token)
    assert not result['success']
    result = coupon.get_coupon_timer(token)
    assert result['success']
    clear_database()

def test_claim_coupon_invalid():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    result = coupon.check_for_daily_coupon_reward(token)
    assert result['success']
    result = coupon.claim_coupons(token)
    assert not result['success']

    clear_database()

def test_add_claimable_token():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    user = get_user_with_token(token, users)
    assert len(user['claimable_coupons']) == 0
    coupon.add_claimable_coupon_to_user(token, 0.1)
    user = get_user_with_token(token, users)
    assert len(user['claimable_coupons']) == 1
    assert user['claimable_coupons'][0]['discount_value'] == 0.1
    assert coupon.str_to_datetime(user['claimable_coupons'][0]['expiry_date']) > datetime.now()

    clear_database()

def test_claim_coupon():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    result = coupon.check_for_daily_coupon_reward(token)
    coupon.add_claimable_coupon_to_user(token, 0.1)
    result = coupon.claim_coupons(token)
    assert result['success']
    user = get_user_with_token(token, users)
    assert len(user['claimed_coupons']) == 1
    assert user['claimed_coupons'][0]['id'] == 0
    assert user['claimed_coupons'][0]['discount_value'] == 0.1

    clear_database()

def test_claim_coupons():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    coupon.add_claimable_coupon_to_user(token, 0.1)
    coupon.add_claimable_coupon_to_user(token, 0.1)
    coupon.add_claimable_coupon_to_user(token, 0.1)
    user = auth.get_user_with_token(token, users)
    assert len(user['claimable_coupons']) == 3
    coupon.claim_coupons(token)

    clear_database()

def test_apply_coupons():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    coupon.add_claimable_coupon_to_user(token, 0.1)
    coupon.add_claimable_coupon_to_user(token, 0.1)
    coupon.add_claimable_coupon_to_user(token, 0.1)
    user = auth.get_user_with_token(token, users)
    coupon.claim_coupons(token)

    user = auth.get_user_with_token(token, users)

    no_coupons = coupon.apply_coupons(60, [])
    assert no_coupons == coupon.apply_coupons(60, [])

    discounted_price = coupon.apply_coupons(60, user['claimed_coupons'])
    assert discounted_price == 60 * 0.9 * 0.9 * 0.9
    clear_database()


def test_process_used_coupons():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    coupon.add_claimable_coupon_to_user(token, 0.1)
    coupon.add_claimable_coupon_to_user(token, 0.1)
    coupon.add_claimable_coupon_to_user(token, 0.1)
    user = auth.get_user_with_token(token, users)
    assert user['claimable_coupons']
    coupon.claim_coupons(token)

    user = auth.get_user_with_token(token, users)

    result = coupon.process_used_coupons(token, user['claimed_coupons'])
    assert result['success']
    user = auth.get_user_with_token(token, users)
    assert len(user['claimed_coupons']) == 0

def test_has_claimable_coupons():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    assert not coupon.has_claimable_coupon(token)
    coupon.add_claimable_coupon_to_user(token, 0.1)
    assert coupon.has_claimable_coupon(token)

    clear_database()