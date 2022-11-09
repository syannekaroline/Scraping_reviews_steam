from base64 import encode
import requests
import json 
from bs4 import BeautifulSoup
from openpyxl import Workbook

def get_app_id(game_name):
    ''' Função que recebe como parâmetro o nome de um jogo da plataforma steam e retorna seu número de idêntificação correnpondente'''

    response = requests.get(url=f'https://store.steampowered.com/search/?term={game_name}&category1=998', headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    app_id = soup.find(class_='search_result_row')['data-ds-appid']

    return app_id

def get_reviews(appid, params={'json':1}):
    ''' Função que realiza a raspagem de reviews e os retorna como uma classe json'''
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url+appid, params=params, headers={'User-Agent': 'Mozilla/5.0'})
    return response.json()

def get_n_reviews(appid, n=260):
    ''' Função que recebe como parâmetro o ID de um jogo e o número de reviews que se quer coletar (padrão n = 260 - max)'''

    reviews = [] 
    cursor = '*' 
    params = { 
            'json' : 1, 
            'filter' : 'all', 
            'language' : 'brazilian', 
            'day_range' : 9223372036854775807, 
            'review_type' : 'all', 
            'purchase_type' : 'all' 
            } # link sobre os parâmetros : https://partner.steamgames.com/doc/store/getreviews

    while n > 0: 
        params['cursor'] = cursor.encode() 
        params['num_per_page'] = min(260, n) 
        n -= 100 

        response = get_reviews(appid, params) 
        cursor = response['cursor'] 
        reviews += response['reviews'] 

        if len(response['reviews']) < 100: break 

    return reviews

def only_review(arquivo="sample.json"):
    '''Função que retorna uma lista apenas com as reviews coletadas do arquivo JSON que recebe como parâmetro'''

    with open(arquivo, encoding='utf-8') as meu_json:
        dados = json.load(meu_json)
    reviews =list()

    for i in dados:
        reviews.append(i['review'])
    print("Número de Reviews coletadas: ",len(reviews))

    return  reviews

def table_DataBase(list):
    ''' Função que insere em uma tabela os comentários coletados'''

    arquivo= Workbook()
    plan0=arquivo.active

    plan0.title = "DataBase"
    plan0.sheet_properties.tabCOLOR = "1079BA"
    arquivo.save("database.xlsx")
    plan0["A1"]="Comentários"

    for i in range (len(list)) :    
        plan0[f"A{i+2}"]= list[i]
            
    arquivo.save("database.xlsx")


####################### execução ##########################
id_game=get_app_id("Last Day of June")
print(f"ID obtido:{id_game}")

reviews = get_n_reviews(id_game,260)

#escrever/armazenar os dados em um arquivo "sample.json"
json_object = json.dumps(reviews, indent = 4,ensure_ascii = False) 
with open("sample.json", "w") as outfile: 
    outfile.write(json_object) 

reviews_list = only_review("sample.json")

table_DataBase(reviews_list)