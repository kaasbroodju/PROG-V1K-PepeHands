import arcade
from enum import Enum
import functions
import api
import random


# Set up the constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = int(WINDOW_WIDTH / 4 * 3)
WINDOW_TITLE = "Marvel"
WINDOW_BACKGROUND_COLOR = arcade.color.BLACK


class State(Enum):
    title_screen = 0
    mode = 1
    choose_difficulty = 2
    leaderboard = 3
    easy = 4
    hard = 5
    score_display = 6


class Background(arcade.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite)
        self.center_x = x
        self.center_y = y
    
    def draw(self):
        arcade.draw_texture_rectangle(WINDOW_WIDTH /2 , WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT, self.texture, 0)


class hintButton(arcade.Sprite):
    '''
    A button used to get a new hint - simple sprite based button
    '''
    def __init__ (self, x, y, sprite):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite, scale=0.2)
        self.center_x = x
        self.center_y = y
        self.text = 'New Hint'

    def draw_text(self):
        arcade.draw_text(self.text, int(self.center_x), int(self.center_y), arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")


class CharacterButton(arcade.Sprite):
    '''
    A button used to give an answer in easy/multiple choice mode - simple sprite based button
    '''
    def __init__(self, x, y, sprite, name):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite, scale=0.2)
        self.center_x = x
        self.center_y = y
        self.character = name

    def draw_text(self):
        arcade.draw_text(self.character, int(self.center_x), int(self.center_y), arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")


class StateButton(arcade.Sprite):
    '''
    a button that changes the state
    '''
    def __init__(self, x, y, sprite, state, text=''):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite, scale=0.1)
        self.center_x = x
        self.center_y = y
        self.state = state
        self.text = text

    def draw_text(self):
        arcade.draw_text(self.text, int(self.center_x), int(self.center_y), arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")

class Cursor(arcade.Sprite):
    '''invisable cursor as long you dont draw'''
    def __init__(self, x, y, sprite):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite)
        self.center_x = x
        self.center_y = y


class AnswerButton(arcade.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite, scale=0.1)
        self.center_x = x
        self.center_y = y

class MyGame(arcade.Window):
    """ An Arcade game. """
    def __init__(self, width, height, title):
        """ Constructor. """
        super().__init__(width, height, title, resizable=True)
        arcade.set_background_color(WINDOW_BACKGROUND_COLOR)
        self.background = Background(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 'startscherm hoofd-1.png.png')
        self.state = State.title_screen
        self.name = str()
        self.mode_buttons = arcade.SpriteList()
        self.mode_buttons.append(StateButton(WINDOW_WIDTH/4 * 1, WINDOW_HEIGHT/2, 'Button.png', State.choose_difficulty, 'start'))
        self.mode_buttons.append(StateButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/2, 'Button.png', State.leaderboard, 'leaderboard'))
        self.cursor = Cursor(0, 0, '1 pixel voor muis-1.png.png')
        self.submit_name_button = StateButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/2, 'Button.png', State.mode, 'ok')
        self.difficulty_buttons = arcade.SpriteList()
        self.difficulty_buttons.append(StateButton(WINDOW_WIDTH/4 * 1, WINDOW_HEIGHT/2, 'Button.png', State.easy, 'easy'))
        self.difficulty_buttons.append(StateButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/2, 'Button.png', State.hard, 'hard'))
        self.possible_answer_buttons = arcade.SpriteList()
        self.timer = int()
        self.delta_timer = float()
        self.score = 25
        self.characterList = list()
        self.back_to_main_menu_button = StateButton(WINDOW_WIDTH/2, WINDOW_HEIGHT/4 * 3, 'Button.png', State.mode, 'main menu')
        self.leaderboard_list = list() #TODO: list with all the score paired with the names [[name, score], [name, score]] (SUSAN)
        self.description = 'hier komt de hint te staan'
        self.hint_penalty = int()
        self.time_penalty = int()
        self.time_wrong = int()
        self.times_played = int()
        self.hintButton = hintButton(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.5, 'Button.png')
        self.total_score = int()
        self.previous_time_penalty = int()
        self.openAnswer = str()
        self.tempString = str()
        self.charNumber = int()
        self.frameskip = False
        self.notation_button_list = arcade.SpriteList()
        self.frameskip_timer = float()
        self.questionNumber = int()
        self.previousDescription = str()
        self.score_display_timer = int()
        self.correctCharacter = dict()
        self.show_answer_button_timer = False
        self.answer_button_timer = float()




    def on_draw(self):
        """ Called whenever we need to draw the window. """
        #on_draw funcite voor alle verschillende menu's
        arcade.start_render()
        self.background.draw()
        if self.state == State.title_screen:
            arcade.draw_text('name: ' + self.name, WINDOW_WIDTH/12,WINDOW_HEIGHT/2,arcade.color.BLACK, 32, bold=True)
            self.submit_name_button.draw()
            self.submit_name_button.draw_text()
        elif self.state == State.mode:
            for button in self.mode_buttons:
                button.draw()
                button.draw_text()
        elif self.state == State.choose_difficulty:
            arcade.draw_text('difficuly', WINDOW_WIDTH/2, WINDOW_HEIGHT/4 *3.07, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")
            for button in self.difficulty_buttons:
                button.draw()
                button.draw_text()
        elif self.state == State.easy:
            arcade.draw_text('easy', WINDOW_WIDTH/2,WINDOW_HEIGHT/4 *3.07, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text(self.description, int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/4 * 1.75), arcade.color.BLACK, 18, bold=True, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text(str(self.score), WINDOW_WIDTH/2 ,WINDOW_HEIGHT/8 * 2,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text(str(self.timer), WINDOW_WIDTH/2 ,WINDOW_HEIGHT/8 ,arcade.color.BLACK, 36, bold=True)
            for button in self.possible_answer_buttons:
                button.draw()
                button.draw_text()
            self.hintButton.draw()
            self.hintButton.draw_text()
            for button in self.notation_button_list:
                button.draw()
        elif self.state == State.hard:
            arcade.draw_text('hard', WINDOW_WIDTH/2,WINDOW_HEIGHT/4 *3.07, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text(self.description, WINDOW_WIDTH/2,WINDOW_HEIGHT/4 * 2.80,arcade.color.BLACK, 18, bold=True, align="center", anchor_x="center", anchor_y="top")
            arcade.draw_text(str(self.score), WINDOW_WIDTH/4,WINDOW_HEIGHT/4 * 3,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text(str(self.timer), WINDOW_WIDTH/4 * 3,WINDOW_HEIGHT/4 * 3 ,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text('Input: '+ self.openAnswer, WINDOW_WIDTH/8*2.4,WINDOW_HEIGHT/8 * 2 ,arcade.color.BLACK, 24, bold=True)
            for button in self.notation_button_list:
                button.draw()


        elif self.state == State.leaderboard:
            self.back_to_main_menu_button.draw()
            self.back_to_main_menu_button.draw_text()
            if len(self.leaderboard_list) >= 10:
                for i in range(0, 10):
                    if i < 5:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i]['name']) + ': ' + str(self.leaderboard_list[i]['score']), WINDOW_WIDTH/8 * 0.5, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i+1)), arcade.color.WHITE, 22, bold=True)
                    else:
                            arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i]['name']) + ': ' + str(self.leaderboard_list[i]['score']), WINDOW_WIDTH/8 * 6, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i-4)), arcade.color.WHITE, 22, bold=True)

            else:
                for i in range(0, len(self.leaderboard_list)):
                    if i < 5:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i]['name']) + ': ' + str(self.leaderboard_list[i]['score']), WINDOW_WIDTH/8 * 0.5, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i+1)), arcade.color.WHITE, 22, bold=True)
                    else:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i]['name']) + ': ' + str(self.leaderboard_list[i]['score']), WINDOW_WIDTH/8 * 6, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i - 4)), arcade.color.WHITE, 22, bold=True)

        elif self.state == State.score_display:
            arcade.draw_text('total score ' + str(self.total_score), WINDOW_WIDTH / 2, WINDOW_HEIGHT/ 8 * 5, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text('name ' + self.name, WINDOW_WIDTH / 2, WINDOW_HEIGHT/ 8 * 4, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")



    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second. """
        self.delta_timer += delta_time
        if self.delta_timer >= 1:
            self.timer += 1
            self.delta_timer = 0
            if self.timer != 0:
                self.time_penalty = self.timer // 10

        if self.time_penalty != self.previous_time_penalty:
            if self.score <= 0:
                self.score = 0
            else:
                self.score -= 1
            self.previous_time_penalty = self.time_penalty
        
        if self.score <= 0 and self.state == State.easy:
            self.score = 25
            self.questionNumber += 1
            if self.questionNumber < 6:
                functions.newMultipleChoice(self)
            else:
                self.questionNumber = 0
                self.state = State.score_display
            self.notation_button_list = arcade.SpriteList()

        if self.frameskip and self.state == State.easy and self.frameskip_timer > 0.2:
            self.frameskip = False
            self.frameskip_timer = float()
            functions.newMultipleChoice(self)
        elif self.frameskip:
            self.frameskip_timer += delta_time

        if self.state == State.score_display:
            self.score_display_timer += delta_time
            if self.score_display_timer > 7:
                self.state = State.leaderboard
                self.score_display_timer = 0
                functions.write_to_json(self.name, self.total_score)
                self.total_score = 0
                self.leaderboard_list = functions.get_leaderboard()
                self.leaderboard_list = functions.sort_leaderbord(self.leaderboard_list)
                self.leaderboard_list.reverse()

        if self.score <= 0 and self.state == State.hard:
            self.score = 25
            self.questionNumber += 1
            if self.questionNumber < 6:
                self.correctCharacter = api.get_character(True)
                self.description = self.correctCharacter['desc']['desc']
                self.charNumber = 0
                for char in self.description:
                    if self.charNumber >= 30 and char == ' ':
                        self.tempString += '\n'
                        self.charNumber = 0
                    self.tempString += char
                    self.charNumber += 1
                self.description = self.tempString
                self.tempString = ''
                #self.notation_button_list = arcade.SpriteList()
                self.total_score += self.score
                self.score = 25
                self.frameskip = False
                self.questionNumber += 1
                self.frameskip_timer = 0.0
                self.timer = 0
            else:
                self.questionNumber = 0
                self.state = State.score_display
            self.notation_button_list = arcade.SpriteList()
            self.answer_button_timer = 0.0

        if self.state == State.hard:
            if self.show_answer_button_timer:
                self.answer_button_timer += delta_time

            if self.answer_button_timer > 2 and self.show_answer_button_timer:
                self.notation_button_list = arcade.SpriteList()
                self.answer_button_timer = 0.0

            if self.frameskip and self.frameskip_timer > 0.2:
                if self.questionNumber < 6:
                    self.correctCharacter = api.get_character(True)
                    self.description = self.correctCharacter['desc']['desc']
                    self.charNumber = 0
                    for char in self.description:
                        if self.charNumber >= 30 and char == ' ':
                            self.tempString += '\n'
                            self.charNumber = 0
                        self.tempString += char
                        self.charNumber += 1
                    self.description = self.tempString
                    self.tempString = ''
                    #self.notation_button_list = arcade.SpriteList()
                    self.total_score += self.score
                    self.score = 25
                    self.frameskip = False
                    self.questionNumber += 1
                    self.frameskip_timer = 0.0
                    self.timer = 0
                else:
                    self.questionNumber = 0
                    self.state = State.score_display



        
    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if self.state == State.title_screen:

            if key != arcade.key.BACKSPACE and chr(key).lower() in 'abcdefghijklmnopqrstuvwxyz1234567890-. ' and len(self.name) < 10: #geen back space en filter
                if modifiers == 17 or modifiers == 1: #shift voor hoofdletter
                    self.name += str(chr(key)).upper()
                else:
                    self.name += str(chr(key))
            elif key == arcade.key.BACKSPACE:
                self.name = self.name[:-1]
        elif self.state == State.hard:
            if key != arcade.key.BACKSPACE and chr(key).lower() in 'abcdefghijklmnopqrstuvwxyz1234567890-. ' and len(self.openAnswer) < 21: #geen back space en filter
                if modifiers == 17 or modifiers == 1: #shift voor hoofdletter
                    self.openAnswer += str(chr(key)).upper()
                else:
                    self.openAnswer += str(chr(key))
            elif key == arcade.key.BACKSPACE:
                self.openAnswer = self.openAnswer[:-1]
            
            elif key == arcade.key.ENTER:
                if self.openAnswer == self.correctCharacter['name']:
                    self.frameskip = True
                    self.notation_button_list.append(AnswerButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/8 * 2, 'Correct.png'))
                    self.show_answer_button_timer = True
                else:
                    self.notation_button_list.append(AnswerButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/8 * 2, 'Wrong.png'))
                    self.show_answer_button_timer = True
                    self.score -= 1
                self.openAnswer = ''
            

    def on_key_release(self, key, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.center_x = x
        self.cursor.center_y = y 

    def on_mouse_release(self, x, y, button, modifiers):
        '''Following code is executed whenever a mouse button is released'''
        if self.state == State.mode:    #If we're on main menu
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.mode_buttons)
            for button in cursor_collides_with: #For any button the mouse 'collides with' i.e. the button we clicked on
                self.state = button.state       #We change the state (the screen we're on) to the one of the button
                if self.state == State.leaderboard: #If that state is leaderboard
                    self.leaderboard_list = functions.get_leaderboard()                         #We call our
                    self.leaderboard_list = functions.sort_leaderbord(self.leaderboard_list)    #leaderboard functions
                    self.leaderboard_list.reverse()                                             #so that we can draw the leaderboard (happens in on_draw)
        elif self.state == State.title_screen:  #If we're on the title screen
            if arcade.check_for_collision(self.cursor, self.submit_name_button) and len(self.name) >= 3:    #Check if name is at least 3 characters and we click on the 'ok' button
                self.state = self.submit_name_button.state #Change state to main menu
        elif self.state == State.choose_difficulty: #If We're on difficulty select screen
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.difficulty_buttons)   #Check for collisions
            for button in cursor_collides_with:
                self.state = button.state #Change state to button state (easy or hard)
                self.timer = 0 #Set the ingame timer 0
                if button.state == State.easy: #If the button state is easy
                    functions.newMultipleChoice(self)   #We call our function that gives us our multiple choice answers/options
                elif button.state == State.hard:    #If the button state is hard
                    self.notation_button_list = arcade.SpriteList() #List of correct and wrong 
                    self.correctCharacter = api.get_character(True) #We get a character + description, this will be correct answer
                    self.description = self.correctCharacter['desc']['desc']    #Save the description of correctcharacter to a variable
                    self.charNumber = 0 #Temp variable
                    for char in self.description:                   #|
                        if self.charNumber >= 30 and char == ' ':   #Add in new lines (\n) on
                            self.tempString += '\n'                 #the next space every 30 characters
                            self.charNumber = 0                     #|
                        self.tempString += char                     #|
                        self.charNumber += 1                        #|
                    self.description = self.tempString              #|
                    self.tempString = ''                            #|
                    self.timer = 0  #Reset timer
        elif self.state == State.easy:  #If we're in gamemode easy
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.possible_answer_buttons)  #Check for collisions
            for button in cursor_collides_with:
                if functions.checkAnswerMultipleChoice(button.character, self.correctCharacter['name']):    #If given answer is correct
                    if self.score < 0:  #If score is somehow under 0
                        self.score = 0  #set score to 0
                    self.total_score += self.score #Add score for this question to total score
                    if self.questionNumber < 6: #If we're not on the last question yet
                        self.notation_button_list.append(AnswerButton(button.center_x, button.center_y, 'Correct.png')) #Add the correct checkmark
                        self.timer = 0  #Reset timer
                        self.delta_timer = 0    #Reset timer
                        self.questionNumber += 1    #Add on to question number
                        self.frameskip = True   #Timing stuff to make sure that the checkmark appears before we start contacting the api
                        self.score = 26 #1 point is removed at start of new question, compensate with increasing score by 1 beforehand
                    else:   #That was the last question
                        self.questionNumber = 0 #Reset question number for next round
                        self.state = State.score_display    #Move on to score screen
                else:   #If answer is not correct
                    if self.score <= 0: #Make sure 
                        self.score = 0  #score doesnt go under 0
                    else:
                        self.score -= 1 #Deduct 1 from score
                    self.notation_button_list.append(AnswerButton(button.center_x, button.center_y, 'Wrong.png'))   #Add wrong mark
            if arcade.check_for_collision(self.cursor, self.hintButton):    #Check for collision
                self.previousDescription                                                                                                                    #
                while True:                                                                                                                                 #
                    comicOrSeries = random.randint(0, 1)                                                                                                    #Make sure we get good
                    if comicOrSeries == 0 and len(self.correctCharacter['desc']['comics'])-1 >= 1:                                                          #hints that are not
                        self.description = self.correctCharacter['desc']['comics'][random.randint(0, len(self.correctCharacter['desc']['comics'])-1)]       #the same as the last one
                        if self.description == self.previousDescription:                                                                                    #
                            continue                                                                                                                        #
                        break                                                                                                                               #
                    elif comicOrSeries == 0 and len(self.correctCharacter['desc']['series'])-1 >= 1:                                                        #
                        self.description = self.correctCharacter['desc']['series'][random.randint(0, len(self.correctCharacter['desc']['series'])-1)]       #
                        if self.description == self.previousDescription:                                                                                    #
                            continue                                                                                                                        #
                        break                                                                                                                               #
                self.charNumber = 0                                 #|
                for char in self.description:                       #|
                    if self.charNumber >= 30 and char == ' ':       #Add in new lines (\n)
                        self.tempString += '\n'                     #the first space after
                        self.charNumber = 0                         #every 30 characters
                    self.tempString += char                         #|
                    self.charNumber += 1                            #|
                self.description = self.tempString                  #|
                self.tempString = ''                                #|
                
                if self.score > 0:    #If score is great than zero
                    self.score -= 3   #Decut 3 from score

        elif self.state == State.leaderboard:   #If we're on leaderboard screen
            if arcade.check_for_collision(self.cursor, self.back_to_main_menu_button):  #Check for collision
                self.state = self.back_to_main_menu_button.state #Go back to main menu if we click on back button
     

def main():
    """ Create an instance of our game window and start the Arcade game loop. """
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()

# only start the game if this script is executed as the main process
if __name__ == "__main__":
    main()