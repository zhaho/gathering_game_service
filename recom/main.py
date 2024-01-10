import xmltodict, json, requests, time, logging, re, os
from collections import Counter
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from sys import stdout

# Prerequisities
load_dotenv()

# Constants
LOG_FORMAT = "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"
games_in_collection_required = 10
top_categories_amount = 10

# Setup Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console Handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(consoleHandler)

# Log Message
logger.info('Script is running')

def json_array(api_url,endpoint):
    cat_list = []
    logger.info("retrieving json array")

    url = api_url + endpoint
    print(url)
    req = requests.get(url)
    json_array = req.content
    
    return json_array

def get_top_user_cats(json_data,top_amount):
    # Extract categories and count their occurrences
    categories = [category.strip() for entry in json_data for category in entry["category"].split(", ")]
    category_counts = Counter(categories)

    # Get top 10 categories
    top_10_categories = category_counts.most_common(top_amount)

    result_categories = []
    for category, count in top_10_categories:
        result_categories.append(category)
    
    return result_categories


def filter_objects_by_categories(json_array, target_categories):
    # Load the JSON data
    data = json.loads(json_array)

    # Split categories in each item and create a set of unique categories
    all_categories = set()
    for item in data:
        categories = item['category'].split(', ')
        all_categories.update(categories)

    # Find the object_ids that have the specified categories
    result_object_ids = []
    for item in data:
        categories = item['category'].split(', ')
        if any(category in target_categories for category in categories):
            result_object_ids.append(item['object_id'])

    return result_object_ids[:30]

def list_users():
    cat_list = []
    logger.info("retrieving users")

    api_url = os.getenv("GATHERING_API_EVENTS_URL")
    endpoint = os.getenv("GATHERING_API_CATS_ENDPOINT")
    url = api_url + endpoint
    
    req = requests.get(url)
    json_array = req.content
    
    return json_array

if __name__ == "__main__":
    while True:
        
        users = json.loads(list_users())
        for user in users:
            logger.info("get data for user "+user["id"])
            cats_array = json_array(api_url = os.getenv("GATHERING_API_URL"), endpoint = os.getenv("GATHERING_API_USERS_ENDPOINT")+"/"+user["id"])
            user_cats_array = json.loads(cats_array)
            #print(user_cats_array)
            # If enough games in collection
            if len(user_cats_array) > games_in_collection_required:
                top_user_cats = get_top_user_cats(json_data=user_cats_array,top_amount=top_categories_amount)
                result = filter_objects_by_categories(json_array(api_url = os.getenv("GATHERING_API_URL"), endpoint = os.getenv("GATHERING_API_ENDPOINT")), top_user_cats)
                print("Games for this user is these:",result)
            
            #print(get_user_categories(user_cats_array))
            # unique the array with top cats
            # user filter function and use the top cats along with the total data
            
        
        
        #result = filter_objects_by_categories(json_array(api_url = os.getenv("GATHERING_API_URL"), endpoint = os.getenv("GATHERING_API_ENDPOINT")), ['Card Game', 'Number', 'Fantasy'])
        #print("Object IDs with specified categories:", result)
        time.sleep(86400)
    