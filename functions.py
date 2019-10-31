import random
import api

#{'name':iron,'desc':{description:'', comics:[]}
#API dataset template^


#def modeSelection(easy):
#    '''Should be called with argument True for easy, '''

#    return


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


def getHint(prevHintType):
    '''Takes previous hint type, returns list of [hint, hintType], first hint always description'''
    
    hintTypes = ['Description', 
    
    return

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
