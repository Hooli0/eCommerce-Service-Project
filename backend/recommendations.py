import pymongo
import database
import json
import random
import auth
import numpy
from server import all_tags

'''
    Records the user clicking on a certain item so that recommendations can be updated
    Parameters:
        token (int): token corresponding to the user to display recommendations for
        item_id (int): the id of the item that was clicked on
    Returns:
        success (bool): whether the operation was successful or not
'''
def record_user_clicked_item(token: str, item_id: int):
    decoded = auth.decode_token(token)
    user_id = decoded['user_id']
    user_id_query = database.users.find_one({"user_id": int(user_id)})
    token_check = database.user_tokens.find_one({"token": token})

    # If token is not valid, return faiure
    if user_id_query is None or token_check is None:
        return {
            'success': False,
            'message': "Invalid Token",
            'userID': user_id
        }

    # Get item from database
    item_query = {"item_id": item_id}
    clicked_item = database.items.find_one(item_query)
    if clicked_item is None:
        return {
            "success": False,
            "message": "Item not found."
        }
    
    # Get user data from database
    user_query = {"user_id": user_id}
    user = database.users.find_one(user_query)
    if user is None:
        return {
            "success": False,
            "message": "User does not exist"
        }

    tag_data = user["tag_data"]
    clicked_tags = clicked_item["tags"]
    number_of_tags = len(clicked_tags)

    for tag in tag_data:
        if tag in clicked_tags:
            # if one of the clicked item's tags already exists, add more priority to it
            tag_data[tag] += 1
            clicked_tags.remove(tag)

    # add new tags
    for tag in clicked_tags:
        tag_data[tag] = 1

    # update number of tags examined - used for normalisation in vector calculation
    new_number_of_tags_clicked = user['number_of_tags_clicked'] + number_of_tags
    new_value = {"$set": {"tag_data": tag_data, 'number_of_tags_clicked': new_number_of_tags_clicked}}
    database.users.update_one(user_query, new_value)

    return {
        "success": True
    }

'''
    Returns a list of item ids that are recommended for a user
    Parameters:
        token (int): token corresponding to the user to display recommendations for
        number_of_recs (int): the maximum number of recommendations to return
    Returns:
        success (bool): whether the operation was successful or not
        item_ids (list of int): the item ids of the related items found
'''
def generate_recs_for_user(token: str, number_of_recs: int):
    decoded = auth.decode_token(token)
    user_id = decoded['user_id']
    user_id_query = database.users.find_one({"user_id": int(user_id)})
    token_check = database.user_tokens.find_one({"token": token})

    # If token is not valid, return faiure
    if user_id_query is None or token_check is None:
        return {
            'success': False,
            'message': "Invalid Token",
            'userID': user_id
        }
    
    # Check if user exists
    user_query = {"user_id": user_id}
    user = database.users.find_one(user_query)
    if user is None:
        return {
            "success": False,
            "message": "User does not exist"
        }

    # if the user has not clicked any items, show some random items (subject to change, will probably show highest selling items first)
    if user['tag_data'] == {}:
        random_items = list(database.items.aggregate([{ "$sample": { "size": int(number_of_recs) } }]))
        for x in random_items:
            del x['_id']
        return {
            "success": True,
            "item_ids": random_items
        }

    '''
        This content-based recommendation system represents tags as dimensions
        in vector space, with the items as vectors.
        An item with the tag "Sports" would be represented with a vector with magnitude 1
        in the dimension "Sports", and the same goes for any other tags it may have.
        To find recommendations, a "user vector" is constructed using the history of tags
        the user has clicked on, and the item vectors with angles closest to the user vector
        are returned.
    '''

    # The number of dimensions of the vector is equal to the number of tags available
    vector_dimensions = database.all_tags.count_documents({})
    user_vector = numpy.zeros(vector_dimensions)

    # Intended to help avoid database lookups
    tag_to_index = {}

    # Construct the user vector from tags they have clicked on
    tag_data = user['tag_data']
    for tag in tag_data:
        i = get_vector_index(tag, tag_to_index)
        user_vector[i] = tag_data[tag] / float(user['number_of_tags_clicked'])

    # get all items from the database and sort in order of cosine similarity to the user vector
    all_items = list(database.items.find())
    search_results = sorted(all_items, key=lambda item: get_cosine_similarity(item, user_vector, tag_to_index), reverse=True)

    # slice list down to desired number of results
    top_results = search_results[:int(number_of_recs)]

    # clean data before returning (_id does not deserialise)
    id_list = []
    for result in top_results:
        del result['_id']
        id_list.append(dict(result))
    return {
        "success": True,
        "item_ids": id_list
    }

'''
    Helper function to determine "closeness" between users/items
'''
def get_cosine_similarity(item, user_vector, tag_to_index):
    tags = item['tags']
    item_vector = numpy.zeros(len(user_vector))
    for tag in tags:
        i = get_vector_index(tag, tag_to_index)
        item_vector[i] = 1

    dot = numpy.dot(user_vector, item_vector)
    magnitudes = numpy.linalg.norm(user_vector) * numpy.linalg.norm(item_vector)
    if magnitudes == 0:
        return 0
    print(item['item_name'] + ': ' + str(dot/magnitudes))
    return dot/magnitudes

'''
    Helper function to get the index we are using for a tag and update the cache
'''
def get_vector_index(tag: str, tag_to_index: dict):
    i = 0
    if tag in tag_to_index:
        i = tag_to_index[tag]
    else:
        tag_in_database = database.all_tags.find_one({'tag': tag})
        i = tag_in_database['tag_id']
        tag_to_index[tag] = i
    
    return i

'''
    Returns a list of item ids related to a given item
    Parameters:
        item_id (int): the id of the item to use as a base
        number_of_recs (int): the maximum number of recommendations to return
    Returns:
        success (bool): whether the operation was successful or not
        item_ids (list of int): the item ids of the related items found
'''
def generate_recs_from_item(item_id: int, number_of_recs: int):
    # Find the original item in the database
    item_query = {"item_id": item_id}
    src_item = database.items.find_one(item_query)
    if src_item is None:
        return {
            "success": False,
            "message": "Item not found."
        }

    # Do another search of the database for items that have at least one tag contained in the original item
    search_tags = src_item["tags"]
    rec_query = {"item_id": {"$ne": item_id}, "tags": {"$elemMatch": {"$in": search_tags}}}
    search_results = list(database.items.find(rec_query))
    # Shuffle the results for randomness and get only the required number
    random.shuffle(search_results)
    search_results = search_results[:number_of_recs]

    id_list = []
    for result in search_results:
        del result['_id']
        id_list.append(dict(result))
    return {
        "success": True,
        "item_ids": id_list
    }