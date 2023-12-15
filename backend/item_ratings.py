from database import items, users, user_tokens
from auth import decode_token, check_user_exists
import datetime

'''
Format of reviews dictionary
    {
        'user_id': (#int)
        'username': (#string)
        'item_id': (#int)
        'rating': (#int)
        'review': (#string)
        'date': (#string)
    }
'''

'''
    Create a review for an item
    Parameters:
        token (str): token corresponding to user creating review
        item_id (int): id of item to review
        rating (int): user's rating of item out of 5 (but can technically be anything)
        review (str): user's written review of item
    Returns:
        success (bool): whether the review was successfully created or not
'''
def create_review(token: str, item_id: int, rating: int, review: str):
    if review == '':
        return {
            'success': False,
            'message': 'Empty reviews are not permitted'
        }
    
    user_id = decode_token(token)['user_id']

    user = users.find_one({'user_id': int(user_id)})
    if user is None:
        return {
            'success': False,
            'message': 'User does not exist'
        }

    now = datetime.datetime.now()
    review_data = {
        'user_id': int(user_id),
        'username': str(user['username']),
        'item_id': int(item_id),
        'rating': int(rating),
        'review': str(review),
        'date': now.strftime('%d-%m-%Y')
    }

    item_query = {'item_id': int(item_id)}
    item_data = items.find_one(item_query)

    if item_data is None:
        return {
            'success': False,
            'message': 'Item does not exist'
        }

    current_reviews = item_data['reviews']

    # Check if the user has already reviewed this item
    # Can we possibly cut down on this operation?
    for r in current_reviews:
        if r['user_id'] == user_id:
            return {
                'success': False,
                'message': 'User has already reviewed this item'
            }

    current_reviews.append(review_data)
    items.update_one(item_query, { '$set': {'reviews': current_reviews, 'avg_rating': get_average_rating(current_reviews)}})

    return {
        'success': True
    }

'''
    Get reviews for item
    Parameters:
        item_id (int): id of item to get reviews of
    Returns:
        success (bool): whether the review was successfully created or not
        reviews (list): list of review data
        avg_rating (float): the average rating of the item
'''
def get_reviews_for_item(item_id: int):
    item_query = {'item_id': int(item_id)}
    item_data = items.find_one(item_query)

    if item_data is None:
        return {
            'success': False,
            'message': 'Item does not exist'
        }
    
    return {
        'success': True,
        'reviews': item_data['reviews'],
        'avg_rating': item_data['avg_rating']
    }


'''
    Helper function for updating average rating after adding a new review
    Parameters:
        item_id (int): id of item to get average rating of
    Returns:
        (float): the current average rating of the item
'''
def get_average_rating(reviews: list):
    if reviews == []:
        return 0
    
    sum = 0

    for r in reviews:
        sum += r['rating']
    
    sum /= float(len(reviews))
    return sum
    

    

    
