from datetime import datetime
from auth import decode_token, generate_token, hash_password
from backend import auth
import json
from datetime import datetime
from database import clear_database, myclient, mydb, admins, admin_tokens, users, user_tokens

def test_register_admin():
    clear_database()

    result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert result["success"]
    assert result["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(result["token"], admin_tokens)

    clear_database

def test_register_two_admins():
    clear_database()

    result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert result["success"]
    assert result["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(result["token"], admin_tokens)

    result2 = auth.auth_register_admin("Jon", "Jones", "JonJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert result2["success"]
    assert result2["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(result2["token"], admin_tokens)

    clear_database()

def test_register_three_admins():
    clear_database()

    result = auth.auth_register_admin("a", "a", "a", "a@a.com", "password", admins, admin_tokens)
    assert result["success"]
    assert result["token"] is not None
    assert auth.check_user_exists("a", admins)
    assert auth.check_token_exists(result["token"], admin_tokens)

    result2 = auth.auth_register_admin("b", "b", "b", "b@b.com", "password", admins, admin_tokens)
    assert result2["success"]
    assert result2["token"] is not None
    assert auth.check_user_exists("b", admins)
    assert auth.check_token_exists(result2["token"], admin_tokens)

    result3 = auth.auth_register_admin("c", "c", "c", "c@c.com", "password", admins, admin_tokens)
    assert result3["success"]
    assert result3["token"] is not None
    assert auth.check_user_exists("c", admins)
    assert auth.check_token_exists(result3["token"], admin_tokens)

    clear_database()

def test_register_user():
    clear_database()

    result = auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    assert result["success"]
    assert result["token"] is not None
    assert auth.check_user_exists("BobJones", users)
    assert auth.check_token_exists(result["token"], user_tokens)

    clear_database()

def test_register_two_users():
    clear_database()

    result = auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    assert result["success"]
    assert result["token"] is not None
    assert auth.check_user_exists("BobJones", users)
    assert auth.check_token_exists(result["token"], user_tokens)

    result2 = auth.auth_register_user("Jon", "Jones", "JonJones", "email@emailthing.com", "password", users, user_tokens)
    assert result2["success"]
    assert result2["token"] is not None
    assert auth.check_user_exists("BobJones", users)
    assert auth.check_token_exists(result2["token"], user_tokens)

    clear_database()

def test_register_three_users():
    clear_database()

    result = auth.auth_register_user("a", "a", "a", "a@a.com", "password", users, user_tokens)
    assert result["success"]
    assert result["token"] is not None
    assert auth.check_user_exists("a", users)
    assert auth.check_token_exists(result["token"], user_tokens)

    result2 = auth.auth_register_user("b", "b", "b", "b@b.com", "password", users, user_tokens)
    assert result2["success"]
    assert result2["token"] is not None
    assert auth.check_user_exists("b", users)
    assert auth.check_token_exists(result2["token"], user_tokens)

    result3 = auth.auth_register_user("c", "c", "c", "c@c.com", "password", users, user_tokens)
    assert result3["success"]
    assert result3["token"] is not None
    assert auth.check_user_exists("c", users)
    assert auth.check_token_exists(result3["token"], user_tokens)

    clear_database()

def test_register_fail_email():
    clear_database()

    result = auth.auth_register_admin("Bob", "Jones", "BobJones", "this is not an email lol", "password", admins, admin_tokens)
    assert not result["success"]
    assert not auth.check_user_exists("BobJones", admins)
    clear_database()

def test_register_fail_username():
    clear_database()

    result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert result["success"]
    assert result["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(result["token"], admin_tokens)

    fail_result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert not fail_result["success"]
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(result["token"], admin_tokens)
    clear_database()

def test_logout():
    clear_database()

    register_result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert register_result["success"]
    assert register_result["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(register_result["token"], admin_tokens)

    logout_result = auth.auth_logout(register_result["token"], admins, admin_tokens)
    assert logout_result["success"]
    assert auth.check_user_exists("BobJones", admins)
    assert not auth.check_token_exists(register_result["token"], admin_tokens)

    clear_database()

def test_logout_fail_nonexistent():
    clear_database()

    register_result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert register_result["success"]
    assert register_result["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(register_result["token"], admin_tokens)

    logout_result = auth.auth_logout({"token": "lolololol"}, admins, admin_tokens)
    assert not logout_result["success"]

    clear_database()

def test_login():
    clear_database()

    register_result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert register_result["success"]
    assert register_result["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(register_result["token"], admin_tokens)

    logout_result = auth.auth_logout(register_result["token"], admins, admin_tokens)
    assert logout_result["success"]
    assert auth.check_user_exists("BobJones", admins)
    assert not auth.check_token_exists(register_result["token"], admin_tokens)

    login_result = auth.auth_login("BobJones", "password", admins, admin_tokens)
    assert login_result["success"]

    decoded = auth.decode_token(login_result["token"])
    assert decoded["user_id"] == 0

    clear_database()

def test_login_fail_password():
    clear_database()

    register_result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert register_result["success"]
    assert register_result["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(register_result["token"], admin_tokens)

    logout_result = auth.auth_logout(register_result["token"], admins, admin_tokens)
    assert logout_result["success"]
    assert auth.check_user_exists("BobJones", admins)
    assert not auth.check_token_exists(register_result["token"], admin_tokens)

    login_result = auth.auth_login("BobJones", "lol", admins, admin_tokens)
    assert not login_result["success"]

    clear_database()

def test_login_fail_username():
    clear_database()

    register_result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    assert register_result["success"]
    assert register_result["token"] is not None
    assert auth.check_user_exists("BobJones", admins)
    assert auth.check_token_exists(register_result["token"], admin_tokens)

    logout_result = auth.auth_logout(register_result["token"], admins, admin_tokens)
    assert logout_result["success"]
    assert auth.check_user_exists("BobJones", admins)
    assert not auth.check_token_exists(register_result["token"], admin_tokens)

    login_result = auth.auth_login("AYAYA", "password", admins, admin_tokens)
    assert not login_result["success"]

    clear_database()

def test_user_details():
    clear_database()

    register_result = auth.auth_register_user("Bob", "Jones", "BobJones", "email@emailthing.com", "password", users, user_tokens)
    assert register_result["success"]
    assert register_result["token"] is not None
    assert auth.check_user_exists("BobJones", users)
    assert auth.check_token_exists(register_result["token"], user_tokens)

    details_result = auth.get_user_details(register_result["token"], users, user_tokens)
    assert details_result["success"]
    obj = json.loads(details_result["details"])
    assert obj["first_name"] == "Bob"
    assert obj["last_name"] == "Jones"
    assert obj["username"] == "BobJones"
    assert obj["email"] == "email@emailthing.com"
    assert obj["cart"] == []
    clear_database()

def test_change_username():
    clear_database()

    register_result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    change_username_result = auth.change_username("Yeeties", register_result["token"], admins, admin_tokens)
    assert change_username_result["message"] == "Successfully changed username"
    assert change_username_result["success"]
    details_result = auth.get_admin_details(register_result["token"], admins, admin_tokens)
    assert details_result["success"]
    obj = json.loads(details_result["details"])
    assert obj["first_name"] == "Bob"
    assert obj["last_name"] == "Jones"
    assert obj["username"] == "Yeeties"
    assert obj["email"] == "email@emailthing.com"
    clear_database()

def test_change_password():
    clear_database()

    register_result = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    change_username_result = auth.change_password("lolololol", register_result["token"], admins, admin_tokens)
    assert change_username_result["message"] == "Successfully changed password"
    assert change_username_result["success"]
    password = hash_password("lolololol")
    decoded = decode_token(register_result["token"])
    query = admins.find_one({"user_id":decoded["user_id"]})
    assert query["password"] == password

    clear_database()

def test_change_password_multiple_entries():
    clear_database()

    register_result_1 = auth.auth_register_admin("Bob", "Jones", "BobJones", "email@emailthing.com", "password", admins, admin_tokens)
    register_result_2 = auth.auth_register_admin("Johnny", "John", "JohnnyJohn", "inspiration@emailthing.com", "password2", admins, admin_tokens)
    register_result_2 = auth.auth_register_admin("Dog", "Cat", "DogCat", "DogCat@emailthing.com", "password3", admins, admin_tokens)
    change_username_result = auth.change_password("lolololol", register_result_1["token"], admins, admin_tokens)
    assert change_username_result["message"] == "Successfully changed password"
    assert change_username_result["success"]
    password = hash_password("lolololol")
    decoded = decode_token(register_result_1["token"])
    query = admins.find_one({"user_id":decoded["user_id"]})
    assert query["password"] == password

    clear_database()
