### hier wat verschillende opties die getest moeten worden (en moeten worden aangepast naar de correcte objecten ###

charact_dict = get_character()
charact_dict['desc']['desc'].replace(charact_dict['name'], 'this character')


charact_dict = get_character()
print('desc'.replace("name", "This character"+', '+'desc'))

#deze werkt denk ik
    for 'name' in get_character('desc'):
        print('desc'.replace('name', "This character"))


    for 'name' in get_character('name'):
        print('name'.replace('name', "this character"))