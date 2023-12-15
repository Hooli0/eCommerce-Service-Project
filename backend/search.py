import pymongo
import database
import json
import random
import auth
from scraper import get_image_url

def search_item(search_string: str):
    query = {
        "item_name": {
        "$regex": str(search_string),
        "$options" : 'i' # case-insensitive
        }
    }
    results = list(database.items.find(query))

    for item in results:
        del item['_id']
    return {
        'success': True,
        'items': results
    }

def get_all_tags():
    tags = list(database.all_tags.find({}))
    results = []
    for tag in tags:
        del tag['_id']
        results.append(dict(tag))

    return {
        'success': True,
        'tags': results
    }

def get_items_with_tag(tag: str):
    query = {'tags': str(tag)}

    results = list(database.items.find(query))

    print(results)

    for item in results:
        del item['_id']
    return {
        'success': True,
        'items': results
    }