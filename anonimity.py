### hier wat verschillende opties die getest moeten worden (en moeten worden aangepast naar de correcte objecten ###

for character in get_character():
    character.replace(character, "This Character")


charact_dict = get_character()
charact_dict['desc']['desc'].replace(charact_dict['name'], 'this character')


charact_dict = get_character()
print('desc'.replace("name", "This character"+', '+'desc'))


for 'name' in get_character('desc'):
    print('name'.replace('name', "This character"))


