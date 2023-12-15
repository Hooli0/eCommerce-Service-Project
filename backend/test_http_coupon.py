import requests
import json
import auth, coupon
import time
from database import users, user_tokens, clear_database

def test_coupon_timer():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    r = requests.post("http://127.0.0.1:2434//user/check_for_daily_reward", json={"token": token})
    assert r.json()['success']
    r = requests.post("http://127.0.0.1:2434//user/check_for_daily_reward", json={"token": token})
    assert not r.json()['success']
    r = requests.get("http://127.0.0.1:2434//user/coupon_timer", params={"token":token})
    assert r.json()['success']
    print(r.json())
    clear_database()

def test_has_claimable_coupons():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    r = requests.get("http://127.0.0.1:2434//user/has_claimable_coupon", params={"token":token})
    assert not r.json()
    print(r.json())
    coupon.add_claimable_coupon_to_user(token, 0.1)
    r = requests.get("http://127.0.0.1:2434//user/has_claimable_coupon", params={"token":token})
    assert r.json()
    print(r.json())

    clear_database()

def test_check_for_daily_rewards():
    clear_database()

    auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    token = auth.auth_login("BobJones", "password", users, user_tokens)['token']
    r = requests.post("http://127.0.0.1:2434//user/check_for_daily_reward", json={"token": token})
    assert r.json()['success']
    time.sleep(7)
    r = requests.post("http://127.0.0.1:2434//user/check_for_daily_reward", json={"token": token})
    print(r.json()['message'])
    r = requests.get("http://127.0.0.1:2434//user/has_claimable_coupon", params={"token":token})
    assert r.json()

    clear_database()

if __name__ == '__main__':
    test_coupon_timer()
    test_has_claimable_coupons()
    test_check_for_daily_rewards()