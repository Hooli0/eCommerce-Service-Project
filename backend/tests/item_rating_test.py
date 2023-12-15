from backend import auth, spoofer, item_ratings, database

token1 = ''
token2 = ''

def test_rate_item_simple():
    spoofer.spoof_data_lightweight()
    id = auth.auth_login("User1", "password", database.users, database.user_tokens)
    token1 = id['token']
    review_result = item_ratings.create_review(token1, 0, 5, 'i liked it')
    assert(review_result['success'] == True)
    review_check = item_ratings.get_reviews_for_item(0)
    assert(review_check['success'] == True)
    assert(len(review_check['reviews']) == 1)
    assert(review_check['avg_rating'] == 5)

    id2 = auth.auth_login("User2", "password", database.users, database.user_tokens)
    token2 = id2['token']
    review_result2 = item_ratings.create_review(token2, 0, 2, 'it was bad')
    assert(review_result2['success'] == True)
    review_check2 = item_ratings.get_reviews_for_item(0)
    assert(review_check2['success'] == True)
    assert(len(review_check2['reviews']) == 2)
    assert(review_check2['avg_rating'] == 3.5)
    database.clear_database()

def test_rate_non_existent_item():
    spoofer.spoof_data_lightweight()

    id = auth.auth_login("User1", "password", database.users, database.user_tokens)
    token1 = id['token']
    review_result = item_ratings.create_review(token1, 0, 5, 'i liked it')
    assert(review_result['success'] == True)
    review_check = item_ratings.get_reviews_for_item(0)
    assert(review_check['success'] == True)
    assert(len(review_check['reviews']) == 1)
    assert(review_check['avg_rating'] == 5)

    review_result2 = item_ratings.create_review(token1, 0, 5, 'i liked it')
    assert(review_result2['success'] == False)

    review_check2 = item_ratings.get_reviews_for_item(0)
    assert(review_check2['success'] == True)
    assert(len(review_check2['reviews']) == 1)
    assert(review_check2['avg_rating'] == 5)

    database.clear_database()

def test_get_non_existent_reviews():
    spoofer.spoof_data_lightweight()

    review_check = item_ratings.get_reviews_for_item(-1)
    assert(review_check['success'] == False)

    database.clear_database()