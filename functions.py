import random
import api
import marvel
import arcade

#{'name':iron,'desc':{'desc':'', 'comics':[], 'series':[]}
#API dataset template^


def newMultipleChoice(self):
    '''Get new set of options of answer(buttons) for easy/multiple choice mode'''
    self.correctCharacter = api.get_character(True) #Get 'correct character' i.e. the answer we're looking for. Argument True so we get character description, comics and series.
    print(self.correctCharacter)
    self.characterList = [] #Empty character list
    self.possible_answer_buttons = arcade.SpriteList()  #'Empty' our set of answer buttons
    self.characterList.append(self.correctCharacter['name']) #Add the name of the correct character to our list of characters
    self.description = self.correctCharacter['desc']['desc'] #Give variable 'description' the value of the description that belongs to our correct character
    self.charNumber = 0
    for char in self.description:                   #|
        if self.charNumber >= 30 and char == ' ':   #Make sure our description
            self.tempString += '\n'                 #has regular \n's (new lines)
            self.charNumber = 0                     #so the entire thing
        self.tempString += char                     #fits on screen.
        self.charNumber += 1                        #|
    self.description = self.tempString              #|
    self.tempString = ''                            #|
    for i in range(0, 9):
        self.character = api.get_character()    #Get a character name 9 times
        """
        TODO
        naam filteren/anomiseren in descriptions
        
        """
        safety = 0
        while self.character['name'] in self.characterList: #Make sure that the name is not a duplicate
            self.character = api.get_character()            #|
            safety += 1
            if safety == 10: #Make sure we dont infinitely keep requesting from API (daily limit)
                break
        self.characterList.append(self.character['name'])   #Add the character to our list
    random.shuffle(self.characterList)  #Shuffle the character list (to make sure the correct answer isnt always in the same place)
    for index in self.characterList:    #Make a button for every character in characterlist
        if self.characterList.index(index) < 5: #First 5 on the left side
            self.possible_answer_buttons.append(marvel.CharacterButton(marvel.WINDOW_WIDTH/8, marvel.WINDOW_HEIGHT/6 * (self.characterList.index(index) + 1), 'Button.png', index))
        else:   #Following 5 on the right
            self.possible_answer_buttons.append(marvel.CharacterButton(marvel.WINDOW_WIDTH/8*7, marvel.WINDOW_HEIGHT/6 * (self.characterList.index(index) - 4), 'Button.png', index))


def checkAnswerOpen(answerString, correctAnswer):
    '''Checks answer for open/hard mode. Takes; user answer (string), correct answer (string). Returns boolean, True if correct, False if wrong'''
    if answerString == correctAnswer:
        rightAnswer = True
    else:
        rightAnswer = False
    return rightAnswer


def checkAnswerMultipleChoice(answer, correctAnswer):
    '''Checks answer for multiple choice/easy mode. Takes; user answer (string), correct answer (string)'''
    if answer == correctAnswer:
        rightAnswer = True
    else:
        rightAnswer = False
    return rightAnswer


def apiFilter():
    '''Filters API data'''
    return


def anonimisation():
    '''Takes hero's name and removes from any hint text. For example replace with [data redacted].'''
    return


"""
LEGACY Jasper
Implemented elsewere in different form

def points(answer, correctAnswer, easy, hint):
    '''Starts on 25 and removes 1 for every wrong answer, 3 for every hint. Maybe boolean argument for "hint" or smth if false it must be a wrong answer so you remove 1, if true remove 3'''
    if easy == True:              ##checks difficulty##
        rightAnswer = checkAnswerMultipleChoice(answer, correctAnswer)     ##checks answer##
        if hint == True:                ##if hint is asked, subtracts 3 points##
            points = points - 3
        else:
            if rightAnswer == False:        ##checks answer and assigns points depending on the answer##
                points -= 1
    else:                       ##hard##
        checkAnswerOpen(answer, correctAnswer)               ##checks answer##
        if hint == True:                ##if hint is asked, subtracts 3 points##
            points = points - 3
        else:
            if rightAnswer == False:        ##checks answer and assigns points depending on the answer##
                points = points - 1
    return points
"""
