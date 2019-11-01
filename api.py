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
    timestamp = str(time.time())            # get time for time stamp
    private_key = "4fdbc63596bbbad52be7b3e42a548cc9f2b6e80f"    # private key
    public_key = "33ed4e91e1467eb433e2bf85cb71abe7"             # public key

    # encrypt request
    hash = hashlib.md5( (timestamp+private_key+public_key).encode('utf-8') )
    md5digest = str(hash.hexdigest())

    # conncect with API
    url = standaard
    connection_url = url+"?ts="+timestamp+"&apikey="+public_key+"&hash="+md5digest
    print(connection_url)

    # get json
    response = requests.get(connection_url)

    # return json
    return json.loads(response.text)

def returned_not_zero(json_file, max_previous_number, number):
    '''
    returns a random number and makes sure code can continue without a problem
    json_file = (dict and required)
    max_previous_numer = (int and required)
    number = (int and required)
    '''
    number_has_changed = False
    while True:
        # exits loop when a new number (with changed previous number) is returned
        if json_file[number]['comics']['returned'] == 0:
            # if there were no comics returned search a new comic
            number = random.randint(0, max_previous_number - 1)
            number_has_changed = True
        else:
            # return new interger
            if number_has_changed:
                # return new previous number and new number
                return [number, random.randint(0, json_file[number]['comics']['returned'] - 1)]
            else:
                # return new number
                return random.randint(0, json_file[number]['comics']['returned'] - 1)

def get_character(with_description=False):
    '''
    grabs a charachter out of the Marvel API
    with_description = defalt False (bool optional)
    returns {'name':'iron man', 'desc':{'desc':'', 'comics':[]}}
    '''
    json_file = get_json_file()     # grabs default characters file
    number = random.randint(0, json_file['data']['count'] - 1)  # pick random number
    number2 = returned_not_zero(json_file['data']['results'], json_file['data']['count'], number) # pick random number and make sure number can acces something
    if type(number2) == list: # number 2 is a list. Fix previous number by splitting
        number = number2[0]
        number2 = number2[1]

    # get a json file of a comic
    json_file_comic_methode = get_json_file(json_file['data']['results'][number]['comics']['items'][number2]['resourceURI'])

    # pick random number
    number3 = random.randint(0, json_file_comic_methode['data']['results'][0]['characters']['returned'] -1)

    # get a character sheet
    character_sheet = get_json_file(json_file_comic_methode['data']['results'][0]['characters']['items'][number3]['resourceURI'])

    nonFilteredCharacterName = character_sheet['data']['results'][0]['name']    #Remove the bracketed (real)names
    filteredCharacterName = nonFilteredCharacterName.split(' (')[0]             #that some character names have

    if with_description:    # if function requires to return a description
        while True:         # loop breaks when a valid character has been returned
            if character_sheet['data']['results'][0]['description'] != '' and character_sheet['data']['results'][0]['description'] != ' ': # proceed with this character if the description is not empty
                # zoekt andere character waarbij character in dezelfde comic zat
                list_of_characters_in_comic = list()
                if json_file_comic_methode['data']['results'][0]['characters']['returned'] > 0:
                    for i in range(0, json_file_comic_methode['data']['results'][0]['characters']['returned']):
                        other_character_name = json_file_comic_methode['data']['results'][0]['characters']['items'][i]['name'] 
                        if other_character_name != character_sheet['data']['results'][0]['name']:
                            list_of_characters_in_comic.append('this character appeared in the same comic as ' + other_character_name)

                number5 = random.randint(0, character_sheet['data']['results'][0]['series']['returned'] -1) #kies 1 willekeurige serie anders krijg je heel veel materiaal
                
                series_vervolgd = get_json_file(character_sheet['data']['results'][0]['series']['items'][number5]['resourceURI']) # get a json file of a serie
                
                # zoekt andere character waarbij character in dezelfde serie zat
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
                number = random.randint(0, json_file['data']['count'] - 1) # pick random number
                number2 = returned_not_zero(json_file['data']['results'], json_file['data']['count'], number) # pick random number and make sure number can acces something
                if type(number2) == list: # number 2 is a list. Fix previous number by splitting
                    number = number2[0]
                    number2 = number2[1]

                # get a json file of a comic
                json_file_comic_methode = get_json_file(json_file['data']['results'][number]['comics']['items'][number2]['resourceURI'])
                
                # pick random number
                number3 = random.randint(0, json_file_comic_methode['data']['results'][0]['characters']['returned'] -1)
                
                # get a character sheet
                character_sheet = get_json_file(json_file_comic_methode['data']['results'][0]['characters']['items'][number3]['resourceURI'])

                nonFilteredCharacterName = character_sheet['data']['results'][0]['name']    #Remove the bracketed (real)names
                filteredCharacterName = nonFilteredCharacterName.split(' (')[0]             #that some character names have
    else:
        #return name with empty dictionary
        return {'name':filteredCharacterName, 
                'desc':{'desc':'',
                        'comics':[]}}