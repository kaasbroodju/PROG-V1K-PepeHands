import random

#{'name':iron,'desc':{description:'', comics:[], films:[]}
#API dataset template^


def modeSelection():
    '''Selects mode'''
    return


def checkAnswerOpen(answerString, correctAnswer):
    '''Checks answer for open/normal mode. Takes; user answer (string), correct answer (string). Returns boolean, True if correct, False if wrong'''
    if answerString == correctAnswer:
        rightAnswer = True
    else:
        rightAnswer = False
    return rightAnswer


def checkAnswerMultipleChoice(answer, correctAnswer):
    if answer == correctAnswer:
        rightAnswer = True
    else:
        rightAnswer = False
    return rightAnswer


def apiConversion():
    '''Converts API data to usable data'''
    return


def anonimisation():
    '''Takes hero's name and removes from any hint text. For example replace with [data redacted].'''
    return


def getHint(dataset, prevHintType):
    '''Takes Dataset, previous hint type, returns list of [hint, hintType], first hint always description'''
    hintTypes = ['Description', 'Films', 'Comics', 'etc.']

    return


def points():
    '''Starts on 25 and removes 1 for every wrong answer, 3 for every hint. Maybe boolean argument for "hint" or smth if false it must be a wrong answer so you remove 1, if true remove 3'''
    points = 25
    if difficulty == True:              ##checks difficulty##
        checkAnswerMultipleChoice()     ##checks answer##
        if rightAnswer == False:        ##checks answer and assigns points depending on the answer##
            points = points - 1
        if randomHint():                ##if hint is asked, subtracts 3 points##
            points = points - 3
    if difficulty == False:             ##checks difficulty##
        checkAnswerOpen()               ##checks answer##
        if rightAnswer == False:        ##checks answer and assigns points depending on the answer##
            points = points - 1
        if randomHint():                ##if hint is asked, subtracts 3 points##
            points = points - 3
    return points

