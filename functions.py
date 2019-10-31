import random
import api
import marvel
import arcade

#{'name':iron,'desc':{description:'', comics:[]}
#API dataset template^


#def modeSelection(easy):
#    '''Should be called with argument True for easy, '''

#    return

def newMultipleChoice(self):
    self.correctCharacter = api.get_character(True)
    print(self.correctCharacter)
    self.characterList = []
    self.possible_answer_buttons = arcade.SpriteList()
    self.characterList.append(self.correctCharacter['name'])
    self.description = self.correctCharacter['desc']['desc']
    self.charNumber = 0
    for char in self.description:
        if self.charNumber >= 30 and char == ' ':
            self.tempString += '\n'
            self.charNumber = 0
        self.tempString += char
        self.charNumber += 1
    self.description = self.tempString
    for i in range(0, 9):
        self.character = api.get_character()
        """
        TODO
        naam filteren/anomiseren in descriptions
        
        """
        safety = 0
        while self.character['name'] in self.characterList:
            self.character = api.get_character()
            safety += 1
            if safety == 10: #Make sure we dont infinitely keep requesting from API (daily limit)
                break
        self.characterList.append(self.character['name'])
    print(self.characterList)
    random.shuffle(self.characterList)
    print(self.characterList)
    for index in self.characterList:
        if self.characterList.index(index) < 5:
            self.possible_answer_buttons.append(marvel.CharacterButton(marvel.WINDOW_WIDTH/8, marvel.WINDOW_HEIGHT/6 * (self.characterList.index(index) + 1), 'Button.png', index))
        else:
            self.possible_answer_buttons.append(marvel.CharacterButton(marvel.WINDOW_WIDTH/8*7, marvel.WINDOW_HEIGHT/6 * (self.characterList.index(index) - 4), 'Button.png', index))


def checkAnswerOpen(answerString, correctAnswer):
    '''Checks answer for open/normal mode. Takes; user answer (string), correct answer (string). Returns boolean, True if correct, False if wrong'''
    if answerString == correctAnswer:
        rightAnswer = True
    else:
        rightAnswer = False
    return rightAnswer


def checkAnswerMultipleChoice(answer, correctAnswer):
    '''Checks answer for multiple choice/easy mode. Takes; user answer (int 1-10), correct answer (int 1-10)'''
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
def getHint(prevHintType):
    '''Takes previous hint type, returns list of [hint, hintType], first hint always description'''
    
    hintTypes = ['Description', 
    
    return
"""
"""
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
