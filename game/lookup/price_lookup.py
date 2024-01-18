import urllib, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def game_title(game_title):
    title_found = False
    encode_url = urllib.parse.quote(game_title)
    url = os.getenv("PRICE_LOOKUP_URL")+encode_url

    # retrieving data from URL
    webUrl = urllib.request.urlopen(url)

    # print data from URL
    data = webUrl.read().decode("utf-8")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(data, 'html.parser')

    # Find the specific information you need
    item_div = soup.find('div', class_='searchcell divider itemname')
    if item_div:
        title_element = item_div.find('span', class_='name')
        if title_element:
            title = title_element.find('a').text.strip()
            if title == game_title:
                title_found = True
    
    if title_found: 
        item_div = soup.find('div', class_='searchcell bestprice multibestprice')
        if item_div:
            price_element = item_div.find('span', class_='price')
            if price_element:
                price = price_element.text.strip()[4:].replace(",",".")
                return round(int(float(price)))

    return None