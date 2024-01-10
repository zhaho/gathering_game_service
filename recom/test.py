from collections import Counter

# Your JSON array
json_data = [
    {"object_id": "63706", "category": "Card Game, Number", "mechanic": "Hand Management", "minplayers": "2", "maxplayers": "7", "preferred_players": "4", "playtime": "30", "user_id": "6", "game_id": "63706", "title": "11 nimmt!", "bgg_rank": "3428", "thumbnail_url": "https://cf.geekdo-images.com/OgaW40VSlThd-z7u7NWE3A__thumb/img/gzFC28W99Qv8aiTTlfP47ze02AQ=/fit-in/200x150/filters:strip_icc()/pic648725.jpg", "id": "1", "modified_at": "2023-12-13 08:09:22"},
    {"object_id": "124742", "category": "Bluffing, Card Game, Collectible Components, Science Fiction", "mechanic": "Action Points, Deck Construction, Hand Management, Race, Secret Unit Deployment, Take That, Variable Player Powers", "minplayers": "2", "maxplayers": "2", "preferred_players": "2", "playtime": "45", "user_id": "6", "game_id": "124742", "title": "Android: Netrunner", "bgg_rank": "66", "thumbnail_url": "https://cf.geekdo-images.com/2ewHIIG_TRq8bYlqk0jIMw__thumb/img/IJaOyyQ7Y59tW6nbKbjTMTFt-Ls=/fit-in/200x150/filters:strip_icc()/pic3738560.jpg", "id": "5692", "modified_at": "2023-12-13 08:09:22"}
]

def get_top_user_cats(json_data,top_amount):
    # Extract categories and count their occurrences
    categories = [category.strip() for entry in json_data for category in entry["category"].split(", ")]
    category_counts = Counter(categories)

    # Get top 10 categories
    top_10_categories = category_counts.most_common(top_amount)

    for category, count in top_10_categories:
        print(f"{category}")

get_top_user_cats(json_data,5)