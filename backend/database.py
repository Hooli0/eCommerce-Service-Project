import pymongo
'''
File to store our databases
Please change the client for suitablility
'''

myclient = pymongo.MongoClient("mongodb+srv://Nozama:nozama@cluster0.ntvvg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = myclient["Nozama_James"]
admins = mydb["admins"]
admin_tokens = mydb["admin_tokens"]
users = mydb["users"]
user_tokens = mydb["user_tokens"]
items = mydb["items"]
item_counter = mydb['item_counter']
all_tags = mydb['all_tags']

def clear_database():
    '''
        Clears all data in the current database
    '''
    admins.delete_many({})
    admin_tokens.delete_many({})
    users.delete_many({})
    user_tokens.delete_many({})
    items.delete_many({})
    items.create_index([('item_name', pymongo.TEXT)], default_language='english')
    item_counter.delete_many({})
    all_tags.delete_many({})
