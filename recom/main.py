import xmltodict, json, requests, time, logging, re, os, random
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

def get_json_data(api_url,endpoint):
    cat_list = []
    url = api_url + endpoint
    req = requests.get(url)
    json_array = req.content
    
    return json.loads(json_array)

def get_top_user_cats(json_data,top_amount):
    
    # Extract categories and count their occurrences
    try:
        categories = [category.strip() for entry in json_data for category in entry["category"].split(", ")]
    except:
        print(json_data)
    category_counts = Counter(categories)

    # Get top 10 categories
    top_10_categories = category_counts.most_common(top_amount)

    result_categories = []
    for category, count in top_10_categories:
        result_categories.append(category)
    
    return result_categories



def filter_objects_by_categories(json_array, target_categories):
    # Load the JSON data
    data = json_array

    # Find the object_ids that have the specified categories and count the matches
    matches_count = {}
    for item in data:
        categories = item['category'].split(', ')
        common_categories = [category for category in categories if category in target_categories]
        num_matches = len(common_categories)
        if num_matches > 0:
            matches_count[item['object_id'],num_matches] = {'count': num_matches, 'categories': common_categories}

    # Sort the results based on the number of matches
    sorted_matches = sorted(matches_count.items(), key=lambda x: x[1]['count'], reverse=True)

    # Extract the object_ids from the sorted matches
    result_object_ids = [obj_id for obj_id, _ in sorted_matches]

    games = result_object_ids[:50]  # You can adjust the number of results as needed

    return games

def list_users():
    cat_list = []
    logger.info("retrieving users")

    api_url = os.getenv("GATHERING_API_EVENTS_URL")
    endpoint = os.getenv("GATHERING_API_CATS_ENDPOINT")
    url = api_url + endpoint
    
    req = requests.get(url)
    json_array = req.content
    
    return json.loads(json_array)

def post_data_to_api(user_id, game):
    api_url = os.getenv("GATHERING_API_RECOM_URL")+os.getenv("GATHERING_API_RECOM_ENDPOINT_POST")

    # Create the request body
    request_body = {
        "user_id": int(user_id),
        "object_id": int(game[0]),
        "matches": int(game[1])
    }

    try:
        # Make the POST request
        response = requests.post(api_url, json=request_body)
        time.sleep(1)
        # Check if the request was successful (status code 2xx)
        if response.status_code // 100 != 2:
            logger.error("error posting data: "+response.text)

    except requests.exceptions.RequestException as e:
        logger.error("error making request:"+e)


def truncate_recom_table():
    api_url = os.getenv("GATHERING_TRUNCATE_URL")+os.getenv("GATHERING_TRUNCATE_TOKEN")

    # Make the POST request
    response = requests.post(api_url)

    if response.status_code == 200:
        logger.info("recom table truncated")
    else:
        logger.info("fail to truncate recom table")

if __name__ == "__main__":
    while True:

        # Empty the table of recommendations
        truncate_recom_table()
        
        # Retrieve users
        users = list_users()

        for user in users:
            logger.info("get data for user "+user["id"])
            categories = get_json_data(api_url = os.getenv("GATHERING_API_URL"), endpoint = os.getenv("GATHERING_API_USERS_ENDPOINT")+"/"+user["id"])
            user_cats_array = categories

            # If enough games in collection
            if len(user_cats_array) > games_in_collection_required:
                logger.info("enough games found - proceed")
                top_user_cats = get_top_user_cats(json_data=user_cats_array,top_amount=top_categories_amount)
                games = filter_objects_by_categories(get_json_data(api_url = os.getenv("GATHERING_API_URL"), endpoint = os.getenv("GATHERING_API_ENDPOINT")), top_user_cats)

                for item in games:
                    post_data_to_api(user_id=user["id"],game=item)
                logger.info("all games for "+user["id"]+" processed")
            else:
                logger.info("not enough games in collection - skip")

        time.sleep(86400)
    