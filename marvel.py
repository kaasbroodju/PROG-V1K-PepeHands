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
    #TODO: documenteer class
    '''
    def __init__ (self, x, y, sprite): #Dit moet nog gechecked worden
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite, scale=0.2)
        self.center_x = x
        self.center_y = y
        self.text = 'New Hint'
        
        #getHintOutput = functions.getHint(api.get_character(), previousHintType) #Dataset moet zegmaar de data uit de api zijn met {'name':iron,'desc':{description:'', comics:[], films:[]}
        #previousHintType = getHintOutput[1]                            #Dit moet uitgevoerd worden wanneer op de knop gedrukt wordt            hint = getHintOutput[0]                                        #Eventueel moet ook points() er nog bij maar idunno -Rick
        #currentPoints = functions.points()

    def draw_text(self):
        arcade.draw_text(self.text, int(self.center_x), int(self.center_y), arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")


class CharacterButton(arcade.Sprite):
    '''
    #TODO: documenteer class
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
        self.back_to_main_menu_button = StateButton(WINDOW_WIDTH/4, WINDOW_HEIGHT/4 * 3, 'Button.png', State.mode, 'back to main menu')
        self.leaderboard_list = list() #TODO: list with all the score paired with the names [[name, score], [name, score]] (SUSAN)
        self.description = 'hier komt de hint te staan'
        self.hint_penalty = int()
        self.time_penalty = int()
        self.time_wrong = int()
        self.times_played = int()
        self.hintButton = hintButton(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.5, 'Button.png')
        self.total_score = int()
        self.previous_time_penalty = int()
        self.frameskip = False
        self.notation_button_list = arcade.SpriteList()
        self.frameskip_timer = float()
        self.questionNumber = int()




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
            arcade.draw_text('difficuly', WINDOW_WIDTH/2, WINDOW_HEIGHT/4 *3, arcade.color.BLACK)
            for button in self.difficulty_buttons:
                button.draw()
                button.draw_text()
        elif self.state == State.easy:
            arcade.draw_text('easy', WINDOW_WIDTH/2,WINDOW_HEIGHT/8 * 7,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text(self.description, int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/4 * 2.5), arcade.color.BLACK, 12, bold=True, align="center", anchor_x="center", anchor_y="center", width=int(WINDOW_WIDTH/2.5))
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
            arcade.draw_text('hard', WINDOW_WIDTH/2,WINDOW_HEIGHT/8 * 7,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text(self.description, WINDOW_WIDTH/2,WINDOW_HEIGHT/4 * 2.5,arcade.color.BLACK, 12, bold=True, align="center", anchor_x="center", anchor_y="center", width=WINDOW_WIDTH/2.5)
            arcade.draw_text(str(self.score), WINDOW_WIDTH/4,WINDOW_HEIGHT/4 * 3,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text(str(self.timer), WINDOW_WIDTH/4 * 3,WINDOW_HEIGHT/4 * 3 ,arcade.color.BLACK, 36, bold=True)
            arcade.draw_text('hier komt de usr input te staan', WINDOW_WIDTH/8,WINDOW_HEIGHT/4 ,arcade.color.BLACK, 36, bold=True)



        elif self.state == State.leaderboard:
            self.back_to_main_menu_button.draw()
            self.back_to_main_menu_button.draw_text()
            if len(self.leaderboard_list) >= 10:
                for i in range(0, 10):
                    if i < 5:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i][0]) + ': ' + str(self.leaderboard_list[i][1]), WINDOW_WIDTH/8 * 0.5, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i+1)), arcade.color.BLACK, 22, bold=True)
                    else:
                            arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i][0]) + ': ' + str(self.leaderboard_list[i][1]), WINDOW_WIDTH/8 * 6, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i-4)), arcade.color.BLACK, 22, bold=True)

            else:
                for i in range(0, len(self.leaderboard_list)):
                    if i < 5:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i][0]) + ': ' + str(self.leaderboard_list[i][1]), WINDOW_WIDTH/8 * 0.5, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i+1)), arcade.color.BLACK, 22, bold=True)
                    else:
                        arcade.draw_text(str(i+1) + '. ' + str(self.leaderboard_list[i][0]) + ': ' + str(self.leaderboard_list[i][1]), WINDOW_WIDTH/8 * 6, WINDOW_HEIGHT - (WINDOW_HEIGHT/6 * (i - 4)), arcade.color.BLACK, 22, bold=True)




    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second. """
        self.delta_timer += delta_time
        if self.delta_timer >= 1:
            self.timer += 1
            self.delta_timer = 0
            self.time_penalty = self.timer // 10

        if self.time_penalty != self.previous_time_penalty:
            if self.score <= 0:
                self.score = 0
            else:
                self.score -= 1
            self.previous_time_penalty = self.time_penalty

        if self.frameskip and self.state == State.easy and self.frameskip_timer > 0.2:
            self.frameskip = False
            self.frameskip_timer = float()
            functions.newMultipleChoice(self)
            self.notation_button_list = arcade.SpriteList()
        elif self.frameskip:
            self.frameskip_timer += delta_time

        
    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if self.state == State.title_screen:

            if key != arcade.key.BACKSPACE and chr(key).lower() in 'abcdefghijklmnopqrstuvwxyz1234567890' and len(self.name) < 10: #geen back space en filter
                if modifiers == 17 or modifiers == 1: #shift voor hoofdletter
                    self.name += str(chr(key)).upper()
                else:
                    self.name += str(chr(key))
            elif key == arcade.key.BACKSPACE:
                self.name = self.name[:-1]
        elif self.state == State.hard:
            pass
            """
            TODO:
            wanneer enter is gedrukt kijken of het goed is
            als het goed is na volgende charater
            als fout opnieuw raden (input resetten)
            na 7 keer gespeelt schrijf score in file (en laat laatste score aan player zien)
            """

    def on_key_release(self, key, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.center_x = x
        self.cursor.center_y = y 

    def on_mouse_release(self, x, y, button, modifiers):
        #(TODO) alleen op rechter muis knop
        if self.state == State.mode:
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.mode_buttons)
            for button in cursor_collides_with:
                self.state = button.state
                if self.state == State.leaderboard:
                    """
                    TODO
                    de data opvragen van een json file met scores en name. 
                    En deze data in self.leaderboard_list te zetten, vervolgens deze te sorteren. 
                    met op index 0 de hoogste score en naam in een list vorm.
                    self.leaderboard_list[0] = ['naam van hoogst scorende persoon', (int) score van hoogste scorende persoon]
                    
                    """
                    pass
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
        elif self.state == State.easy:
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.possible_answer_buttons)
            for button in cursor_collides_with:
                if functions.checkAnswerMultipleChoice(button.character, self.correctCharacter['name']):
                    if self.score < 0:
                        self.score = 0
                    self.total_score += self.score
                    if self.questionNumber < 7:
                        self.notation_button_list.append(AnswerButton(button.center_x, button.center_y, 'Correct.png'))
                        self.score = 25
                        self.timer = 0
                        self.delta_timer = 0
                        self.questionNumber += 1
                        self.frameskip = True #TODO morris frameskips shite
                    else:
                        pass #TODO: write name + score to json (susan)
                else:
                    if self.score =< 0:
                        self.score = 0
                    else:
                        self.score -= 1
                    self.notation_button_list.append(AnswerButton(button.center_x, button.center_y, 'Wrong.png'))
                    pass #TODO: make wrong button spritelist append? morris
            

        elif self.state == State.leaderboard:
            if arcade.check_for_collision(self.cursor, self.back_to_main_menu_button):
                self.state = self.back_to_main_menu_button.state
        elif self.state == State.easy:
            """
            TODO
            als op de juiste button word gedrukt dan nieuwe characters zoeken
            als foute button penalty omhoog en wrong button naast de button die is gedrukt
            na 7 keer gespeelt schrijf score in file (en laat laatste score aan player zien)
            """
            pass

def main():
    """ Create an instance of our game window and start the Arcade game loop. """
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()

# only start the game if this script is executed as the main process
if __name__ == "__main__":
    main()