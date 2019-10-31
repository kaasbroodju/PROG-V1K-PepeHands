import time
import hashlib
import requests
import json
import random

def get_json_file(standaard='http://gateway.marvel.com/v1/public/characters'):
    '''
    grabs a json file from the Marvel API
    standaard = http://gateway.marvel.com/v1/public/characters as default (string and optional)
    returns a dictionary
    '''
    timestamp = str(time.time())
    private_key = "2acdb82a84ec3870b21de291b90755ddcb0f6d6b"
    public_key = "28624c577d2a5ae05547164c7f3c06a2"

    #encrypt request
    hash = hashlib.md5( (timestamp+private_key+public_key).encode('utf-8') )
    md5digest = str(hash.hexdigest())

    #conncect with API
    url = standaard
    connection_url = url+"?ts="+timestamp+"&apikey="+public_key+"&hash="+md5digest
    print(connection_url)

    #get json
    response = requests.get(connection_url)
    return json.loads(response.text)

def returned_not_zero(json_file, max_previous_number, nummer):
    '''
    returns a random number and makes sure code can continue without a problem
    json_file = (dict and required)
    max_previous_numer = (int and required)
    nummer = (int and required)
    '''
    nummer_has_changed = False
    while True:
        if json_file[nummer]['comics']['returned'] == 0:
            nummer = random.randint(0, max_previous_number - 1)
            nummer_has_changed = True
        else:
            if nummer_has_changed:
                return [nummer, random.randint(0, json_file[nummer]['comics']['returned'] - 1)]
            else:
                return random.randint(0, json_file[nummer]['comics']['returned'] - 1)

def get_character(with_description=False):
    '''
    grabs a charachter out of the Marvel API
    with_description = defalt False (bool optional)
    returns {'name':'iron man', 'desc':{'desc':'', 'comics':[]}}
    '''
    json_file = get_json_file()
    nummer = random.randint(0, json_file['data']['count'] - 1)
    nummer2 = returned_not_zero(json_file['data']['results'], json_file['data']['count'], nummer)
    if type(nummer2) == list:
        nummer = nummer2[0]
        nummer2 = nummer2[1]
    json_file_comic_methode = get_json_file(json_file['data']['results'][nummer]['comics']['items'][nummer2]['resourceURI'])
    nummer3 = random.randint(0, json_file_comic_methode['data']['results'][0]['characters']['returned'] -1)
    character_sheet = get_json_file(json_file_comic_methode['data']['results'][0]['characters']['items'][nummer3]['resourceURI'])

    nonFilteredCharacterName = character_sheet['data']['results'][0]['name']    #Remove the bracketed (real)names
    filteredCharacterName = nonFilteredCharacterName.split(' (')[0]             #that some character names have

    if with_description:
        while True:
            if character_sheet['data']['results'][0]['description'] != '':
                # zoekt andere character waarbij character in dezelfde comic zat
                list_of_characters_in_comic = list()
                if json_file_comic_methode['data']['results'][0]['characters']['returned'] > 0:
                    for i in range(0, json_file_comic_methode['data']['results'][0]['characters']['returned']):
                        other_character_name = json_file_comic_methode['data']['results'][0]['characters']['items'][i]['name'] 
                        if other_character_name != character_sheet['data']['results'][0]['name']:
                            list_of_characters_in_comic.append('this character appeared in the same comic as ' + other_character_name)

                nummer5 = random.randint(0, character_sheet['data']['results'][0]['series']['returned'] -1) #kies 1 willekeurige serie anders krijg je heel veel materiaal
                
                # zoekt andere character waarbij character in dezelfde serie zat
                series_vervolgd = get_json_file(character_sheet['data']['results'][0]['series']['items'][nummer5]['resourceURI'])
                list_of_characters_in_series = list()
                if series_vervolgd['data']['results'][0]['characters']['returned'] > 0:
                    for i in range(0, series_vervolgd['data']['results'][0]['characters']['returned']):
                        other_character_name = series_vervolgd['data']['results'][0]['characters']['items'][i]['name'] 
                        if other_character_name != character_sheet['data']['results'][0]['name']:
                            list_of_characters_in_series.append('this character appeared in the same storyline as ' + other_character_name)
                
                #geeft dictionary terug
                return {'name':filteredCharacterName, 
                        'desc':{'desc':character_sheet['data']['results'][0]['description'].replace(filteredCharacterName, '[DATA RETRACTED]'),
                                'comics': list_of_characters_in_comic,
                                'series': list_of_characters_in_series}}
            else:
                #zoek nieuw character
                nummer = random.randint(0, json_file['data']['count'] - 1)
                nummer2 = returned_not_zero(json_file['data']['results'], json_file['data']['count'], nummer)
                if type(nummer2) == list:
                    nummer = nummer2[0]
                    nummer2 = nummer2[1]
                json_file_comic_methode = get_json_file(json_file['data']['results'][nummer]['comics']['items'][nummer2]['resourceURI'])
                nummer3 = random.randint(0, json_file_comic_methode['data']['results'][0]['characters']['returned'] -1)
                character_sheet = get_json_file(json_file_comic_methode['data']['results'][0]['characters']['items'][nummer3]['resourceURI'])
                
                nonFilteredCharacterName = character_sheet['data']['results'][0]['name']    #Remove the bracketed (real)names
                filteredCharacterName = nonFilteredCharacterName.split(' (')[0]             #that some character names have
    else:
        #return name with empty dictionary
        return {'name':filteredCharacterName, 
                'desc':{'desc':'',
                        'comics':[]}}

#random.choice([keys()])