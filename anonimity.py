### hier wat verschillende opties die getest moeten worden (en moeten worden aangepast naar de correcte objecten ###

charact_dict = get_character()
charact_dict['desc']['desc'].replace(charact_dict['name'], '[DATA REDACTED]')


charact_dict = get_character()
print('desc'.replace("name", "This character"+', '+'desc'))

#deze werkt denk ik
    for 'name' in get_character('desc'):
        print('desc'.replace('name', "This character"))


    for 'name' in get_character('name'):
        print('name'.replace('name', "this character"))


character_sheet['data']['results'][0]['description'].replace(character_sheet['data']['results'][0]['name'], 'DATA RETRACTED')