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


class State(Enum): #creating the Enum class to translate integers to variable class for the title screen
    title_screen = 0
    mode = 1
    choose_difficulty = 2
    leaderboard = 3
    easy = 4
    hard = 5
    score_display = 6


class Background(arcade.Sprite): #creating the background class for arcade here
    def __init__(self, x, y, sprite): #defining a texture loader
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite)
        self.center_x = x
        self.center_y = y
    
    def draw(self): #defining the draw self function
        arcade.draw_texture_rectangle(WINDOW_WIDTH /2 , WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT, self.texture, 0)


class hintButton(arcade.Sprite): #defining a hint button to request hints at a cost of 3 points
    '''
    A button used to get a new hint - simple sprite based button
    '''
    def __init__ (self, x, y, sprite): #putting the text onto the sprite
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite, scale=0.2)
        self.center_x = x
        self.center_y = y
        self.text = 'New Hint'

    def draw_text(self): #allowing the sprite to draw text on itself
        arcade.draw_text(self.text, int(self.center_x), int(self.center_y), arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")


class CharacterButton(arcade.Sprite): #defining a button that has a marvel character name on it that can be clicked to answer
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

    def draw_text(self): #allowing the sprite to draw text on itself
        arcade.draw_text(self.character, int(self.center_x), int(self.center_y), arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")


class StateButton(arcade.Sprite): #defining a button that changes the state of the game
    '''
    a button that changes the state
    '''
    def __init__(self, x, y, sprite, state, text=''): #defining the state and text on the sprite
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite, scale=0.1)
        self.center_x = x
        self.center_y = y
        self.state = state
        self.text = text

    def draw_text(self): #allowing the sprite to draw text on itself
        arcade.draw_text(self.text, int(self.center_x), int(self.center_y), arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")

class Cursor(arcade.Sprite): #creating an invisible cursor that can be used to track mouse movements until a draw function gets called
    '''invisable cursor as long you dont draw'''
    def __init__(self, x, y, sprite): #defining the texture and position
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite)
        self.center_x = x
        self.center_y = y


class AnswerButton(arcade.Sprite): #defining an answer button
    def __init__(self, x, y, sprite):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite, scale=0.1)
        self.center_x = x
        self.center_y = y

class MyGame(arcade.Window): #here the creation of the game starts
    """ An Arcade game. """
    def __init__(self, width, height, title): #defining all of the functions
        """ Constructor. """
        super().__init__(width, height, title, resizable=True)
        arcade.set_background_color(WINDOW_BACKGROUND_COLOR)

        # miscelanious
        self.state = State.title_screen # which menu has to be drawn
        self.name = str()               # username stored here
        self.characterList = list() 
        self.leaderboard_list = list()  # list of small dictionaries with names and scores
        self.description = 'error'      # show error on places where description is drawn
        self.previous_time_penalty = int()
        self.openAnswer = str()         # type box in hard mode
        self.tempString = str()         # temp srting for filtering description of name that has to be guessed
        self.charNumber = int()
        self.questionNumber = int()     # number of questions answered
        self.previousDescription = str() # new description shouldn't be the same as previous description. previous description is stored here
        self.correctCharacter = dict()  # a dictionary where the correct character is safed in
        
        # boolean
        self.frameskip = False          # enables to draw a (couple of) frame(s) before loading the api
        self.show_answer_button_timer = False

        # buttons and classes
        self.background = Background(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 'startscherm hoofd-1.png.png')    # make background image
        self.hintButton = hintButton(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.5, 'Button.png')                   # hint button for easy mode
        self.back_to_main_menu_button = StateButton(WINDOW_WIDTH/2, WINDOW_HEIGHT/4 * 3, 'Button.png', State.mode, 'main menu')
        
        # buttons for difficulty
        self.difficulty_buttons = arcade.SpriteList()
        self.difficulty_buttons.append(StateButton(WINDOW_WIDTH/4 * 1, WINDOW_HEIGHT/2, 'Button.png', State.easy, 'easy'))
        self.difficulty_buttons.append(StateButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/2, 'Button.png', State.hard, 'hard'))
        
        # buttons for start and leaderboar
        self.mode_buttons = arcade.SpriteList()
        self.mode_buttons.append(StateButton(WINDOW_WIDTH/4 * 1, WINDOW_HEIGHT/2, 'Button.png', State.choose_difficulty, 'start'))
        self.mode_buttons.append(StateButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/2, 'Button.png', State.leaderboard, 'leaderboard'))
        
        self.cursor = Cursor(0, 0, '1 pixel voor muis-1.png.png') # small invisible cursor for collision detection
        self.submit_name_button = StateButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/2, 'Button.png', State.mode, 'ok') # name submit button on title screen
        
        # sprite lists
        self.possible_answer_buttons = arcade.SpriteList()
        self.notation_button_list = arcade.SpriteList()
        
        # counter
        self.time_penalty = int()
        self.questionNumber = int()

        # score
        self.total_score = int()
        self.score = 25

        # timers
        self.frameskip_timer = float()
        self.timer = int()
        self.delta_timer = float()
        self.score_display_timer = int()        
        self.answer_button_timer = float()







    def on_draw(self): #defining how to draw on the game window when called upon
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        self.background.draw()
        if self.state == State.title_screen: #defining how to draw on the title screen
            arcade.draw_text('name: ' + self.name, WINDOW_WIDTH/12,WINDOW_HEIGHT/2,arcade.color.BLACK, 32, bold=True)
            self.submit_name_button.draw()
            self.submit_name_button.draw_text()
        elif self.state == State.mode: #defining the state of the buttons
            for button in self.mode_buttons:
                button.draw()
                button.draw_text()
        elif self.state == State.choose_difficulty: #defining how the program allows you to choose the difficulty
            arcade.draw_text('difficuly', WINDOW_WIDTH/2, WINDOW_HEIGHT/4 *3.07, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")
            for button in self.difficulty_buttons: #defining the difficulty buttons
                button.draw()
                button.draw_text()
        elif self.state == State.easy: #defining what the program has to do when you select easy mode
            arcade.draw_text('easy', WINDOW_WIDTH/2,WINDOW_HEIGHT/4 *3.07, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text(self.description, int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/4 * 1.75), arcade.color.BLACK, 18, bold=True, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text(str(self.score), WINDOW_WIDTH/2 ,WINDOW_HEIGHT/8 * 2,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text(str(self.timer), WINDOW_WIDTH/2 ,WINDOW_HEIGHT/8 ,arcade.color.BLACK, 36, bold=True)
            for button in self.possible_answer_buttons: #defines the possible answer buttons in easy mode
                button.draw()
                button.draw_text()
            self.hintButton.draw()
            self.hintButton.draw_text()
            for button in self.notation_button_list: #draws the button
                button.draw()
        elif self.state == State.hard: #defining what the program has to do when you select hard mode
            arcade.draw_text('hard', WINDOW_WIDTH/2,WINDOW_HEIGHT/4 *3.07, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text(self.description, WINDOW_WIDTH/2,WINDOW_HEIGHT/4 * 2.80,arcade.color.BLACK, 18, bold=True, align="center", anchor_x="center", anchor_y="top")
            arcade.draw_text(str(self.score), WINDOW_WIDTH/4,WINDOW_HEIGHT/4 * 3,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text(str(self.timer), WINDOW_WIDTH/4 * 3,WINDOW_HEIGHT/4 * 3 ,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text('Input: '+ self.openAnswer, WINDOW_WIDTH/8*2.4,WINDOW_HEIGHT/8 * 2 ,arcade.color.BLACK, 24, bold=True)
            for button in self.notation_button_list: #draws the button
                button.draw()


        elif self.state == State.leaderboard: #defines the leaderboard
            self.back_to_main_menu_button.draw()
            self.back_to_main_menu_button.draw_text()
            if len(self.leaderboard_list) >= 10: #creating the dimensions of the leaderboard under condition A
                for i in range(0, 10):
                    if i < 5:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i]['name']) + ': ' + str(self.leaderboard_list[i]['score']), WINDOW_WIDTH/8 * 0.5, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i+1)), arcade.color.WHITE, 22, bold=True)
                    else:
                            arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i]['name']) + ': ' + str(self.leaderboard_list[i]['score']), WINDOW_WIDTH/8 * 6, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i-4)), arcade.color.WHITE, 22, bold=True)

            else: #creating the dimensions of the leaderboard under condition B
                for i in range(0, len(self.leaderboard_list)):
                    if i < 5:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i]['name']) + ': ' + str(self.leaderboard_list[i]['score']), WINDOW_WIDTH/8 * 0.5, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i+1)), arcade.color.WHITE, 22, bold=True)
                    else:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i]['name']) + ': ' + str(self.leaderboard_list[i]['score']), WINDOW_WIDTH/8 * 6, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i - 4)), arcade.color.WHITE, 22, bold=True)

        elif self.state == State.score_display: #defines the state of the scores and displays them
            arcade.draw_text('total score ' + str(self.total_score), WINDOW_WIDTH / 2, WINDOW_HEIGHT/ 8 * 5, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text('name ' + self.name, WINDOW_WIDTH / 2, WINDOW_HEIGHT/ 8 * 4, arcade.color.BLACK, 36, bold=True, align="center", anchor_x="center", anchor_y="center")



    def update(self, delta_time): #defines the refresh rate of the objects in our game
        """ Called to update our objects. Happens approximately 60 times per second. """
        self.delta_timer += delta_time #defining the timer
        if self.delta_timer >= 1:
            self.timer += 1
            self.delta_timer = 0
            if self.timer != 0:
                self.time_penalty = self.timer // 10

        if self.time_penalty != self.previous_time_penalty: #defining the time penalty
            if self.score <= 0:
                self.score = 0
            else:
                self.score -= 1
            self.previous_time_penalty = self.time_penalty
        
        if self.score <= 0 and self.state == State.easy: #defining the game state for easy difficulty
            self.score = 25
            self.questionNumber += 1
            if self.questionNumber < 6:
                functions.newMultipleChoice(self)
            else:
                self.questionNumber = 0
                self.state = State.score_display
            self.notation_button_list = arcade.SpriteList()

        if self.frameskip and self.state == State.easy and self.frameskip_timer > 0.2: #defining how to skip frames in easy mode
            self.frameskip = False
            self.frameskip_timer = float()
            functions.newMultipleChoice(self)
        elif self.frameskip:
            self.frameskip_timer += delta_time

        if self.state == State.score_display: #defining the score display state
            self.score_display_timer += delta_time
            if self.score_display_timer > 7:
                self.state = State.leaderboard
                self.score_display_timer = 0
                functions.write_to_json(self.name, self.total_score)
                self.total_score = 0
                self.leaderboard_list = functions.get_leaderboard()
                self.leaderboard_list = functions.sort_leaderbord(self.leaderboard_list)
                self.leaderboard_list.reverse()

        if self.score <= 0 and self.state == State.hard: #defining how to decide the game state in hard mode
            self.score = 25
            self.questionNumber += 1
            if self.questionNumber < 6: #asks if it's question 6 or before
                self.correctCharacter = api.get_character(True)
                self.description = self.correctCharacter['desc']['desc']
                self.charNumber = 0
                for char in self.description: #defines the char in the description
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

        if self.state == State.hard: #checks if game state is hard
            if self.show_answer_button_timer: #shows the answer button timer in hard mode
                self.answer_button_timer += delta_time

            if self.answer_button_timer > 2 and self.show_answer_button_timer: #checks if the answer button timer is smaller than 2 and if answer button timer is shown
                self.notation_button_list = arcade.SpriteList()
                self.answer_button_timer = 0.0

            if self.frameskip and self.frameskip_timer > 0.2: #checks if the frameskip is true and if frameskip timer is more than 0.2
                if self.questionNumber < 6: #checks if it's earlier than question 6
                    self.correctCharacter = api.get_character(True)
                    self.description = self.correctCharacter['desc']['desc']
                    self.charNumber = 0
                    for char in self.description: #a loop for every char in description
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



        
    def on_key_press(self, key, modifiers): #defining the function that decides what happens upon keypress in the game
        """ Called whenever the user presses a key. """
        if self.state == State.title_screen: #checks if the game state is title screen

            if key != arcade.key.BACKSPACE and chr(key).lower() in 'abcdefghijklmnopqrstuvwxyz1234567890-. ' and len(self.name) < 10: #no back space of filter
                if modifiers == 17 or modifiers == 1: #shift for capital letter
                    self.name += str(chr(key)).upper()
                else:
                    self.name += str(chr(key))
            elif key == arcade.key.BACKSPACE: #checks if a backspace is used
                self.name = self.name[:-1]
        elif self.state == State.hard: #when the game state is hard
            if key != arcade.key.BACKSPACE and chr(key).lower() in 'abcdefghijklmnopqrstuvwxyz1234567890-. ' and len(self.openAnswer) < 21: #no back space of filter
                if modifiers == 17 or modifiers == 1: #shift for capital letter
                    self.openAnswer += str(chr(key)).upper()
                else:
                    self.openAnswer += str(chr(key))
            elif key == arcade.key.BACKSPACE: #checks if a backspace is used
                self.openAnswer = self.openAnswer[:-1]
            #jshfgkjsdggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
            elif key == arcade.key.ENTER: #defines what happens upon pressing the enter button
                if self.openAnswer == self.correctCharacter['name']: #checks if the answer is equal to the correct answer
                    self.frameskip = True
                    self.notation_button_list.append(AnswerButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/8 * 2, 'Correct.png'))
                    self.show_answer_button_timer = True
                else: #takes away score upon wrong answer
                    self.notation_button_list.append(AnswerButton(WINDOW_WIDTH/4 * 3, WINDOW_HEIGHT/8 * 2, 'Wrong.png'))
                    self.show_answer_button_timer = True
                    self.score -= 1
                self.openAnswer = ''
            """
            TODO:
            wanneer enter is gedrukt kijken of het goed is
            als het goed is na volgende charater
            als fout opnieuw raden (input resetten)
            na 7 keer gespeelt schrijf score in file (en laat laatste score aan player zien)
            """

    def on_key_release(self, key, modifiers): #pass whenever a key is released
        pass

    def on_mouse_motion(self, x, y, dx, dy): #defines some mouse motions by positioning
        self.cursor.center_x = x
        self.cursor.center_y = y 

    def on_mouse_release(self, x, y, button, modifiers):
        #(TODO) alleen op rechter muis knop
        if self.state == State.mode:
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.mode_buttons)
            for button in cursor_collides_with:
                self.state = button.state
                if self.state == State.leaderboard:
                    self.leaderboard_list = functions.get_leaderboard()
                    self.leaderboard_list = functions.sort_leaderbord(self.leaderboard_list)
                    self.leaderboard_list.reverse()
        elif self.state == State.title_screen:
            if arcade.check_for_collision(self.cursor, self.submit_name_button) and len(self.name) >= 3:
                self.state = self.submit_name_button.state
        elif self.state == State.choose_difficulty:
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.difficulty_buttons)
            for button in cursor_collides_with:
                self.state = button.state
                self.timer = 0
                if button.state == State.easy:
                    functions.newMultipleChoice(self)
                elif button.state == State.hard:
                    self.notation_button_list = arcade.SpriteList()
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
                    self.timer = 0
        elif self.state == State.easy:
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.possible_answer_buttons)
            for button in cursor_collides_with:
                if functions.checkAnswerMultipleChoice(button.character, self.correctCharacter['name']):
                    if self.score < 0:
                        self.score = 0
                    self.total_score += self.score
                    if self.questionNumber < 6:
                        self.notation_button_list.append(AnswerButton(button.center_x, button.center_y, 'Correct.png'))
                        self.timer = 0
                        self.delta_timer = 0
                        self.questionNumber += 1
                        self.frameskip = True
                        self.score = 26 #1 point is removed at start of new question, compensate with increasing score by 1 beforehand
                    else:
                        self.questionNumber = 0
                        self.state = State.score_display
                else:
                    if self.score <= 0:
                        self.score = 0
                    else:
                        self.score -= 1
                    self.notation_button_list.append(AnswerButton(button.center_x, button.center_y, 'Wrong.png'))
            if arcade.check_for_collision(self.cursor, self.hintButton):
                self.previousDescription
                while True: 
                    comicOrSeries = random.randint(0, 1)                                                #
                    if comicOrSeries == 0 and len(self.correctCharacter['desc']['comics'])-1 >= 1:                                                          #t
                        self.description = self.correctCharacter['desc']['comics'][random.randint(0, len(self.correctCharacter['desc']['comics'])-1)]       #e
                        if self.description == self.previousDescription:                                                                                    #s
                            continue                                                                                                                        #t
                        break                                                                                                                               #
                    elif comicOrSeries == 0 and len(self.correctCharacter['desc']['series'])-1 >= 1:                                                        #p
                        self.description = self.correctCharacter['desc']['series'][random.randint(0, len(self.correctCharacter['desc']['series'])-1)]       #l
                        if self.description == self.previousDescription:                                                                                    #z
                            continue
                        break
                self.charNumber = 0
                for char in self.description:
                    if self.charNumber >= 30 and char == ' ':
                        self.tempString += '\n'
                        self.charNumber = 0
                    self.tempString += char
                    self.charNumber += 1
                self.description = self.tempString
                self.tempString = ''
                
                if self.score > 0:    
                    self.score -= 3

        elif self.state == State.leaderboard:
            if arcade.check_for_collision(self.cursor, self.back_to_main_menu_button):
                self.state = self.back_to_main_menu_button.state
     

def main():
    """ Create an instance of our game window and start the Arcade game loop. """
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()

# only start the game if this script is executed as the main process
if __name__ == "__main__":
    main()