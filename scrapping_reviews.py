from base64 import encode
import requests
import json 
from bs4 import BeautifulSoup

def get_app_id(game_name):
    response = requests.get(url=f'https://store.steampowered.com/search/?term={game_name}&category1=998', headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    app_id = soup.find(class_='search_result_row')['data-ds-appid']
    return app_id

def get_reviews(appid, params={'json':1}):
        url = 'https://store.steampowered.com/appreviews/'
        response = requests.get(url=url+appid, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        return response.json()

def get_n_reviews(appid, n=100):

    reviews = [] 
    cursor = '*' 
    params = { 
            'json' : 1, 
            'filter' : 'all', 
            'language' : 'brazilian', 
            'day_range' : 9223372036854775807, 
            'review_type' : 'all', 
            'purchase_type' : 'all' 
            } 

    while n > 0: 
        params['cursor'] = cursor.encode() 
        params['num_per_page'] = min(100, n) 
        n -= 100 

        response = get_reviews(appid, params) 
        cursor = response['cursor'] 
        reviews += response['reviews'] 

        if len(response['reviews']) < 100: break 

    return reviews

# print(get_n_reviews('635320'),10)
# id=get_app_id("Last Day of June")
# print(len (get_n_reviews('635320')))
# for n,review in enumerate(get_n_reviews('635320')):
    # print(n,"-",review['review'])
reviews =get_n_reviews('635320')
# for i in dictionary:
json_object = json.dumps(reviews, indent = 4,ensure_ascii = False) 
with open("sample.json", "w") as outfile: 
    outfile.write(json_object) 
