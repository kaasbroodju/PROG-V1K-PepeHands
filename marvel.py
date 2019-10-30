import arcade
from enum import Enum
import functions
import api
import random


# Set up the constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
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
'''
class hintButton(Textbutton):
    def __init__ (self, game, x=0, y=0, width=100, height=40, text="`Hint`", theme=None): #Dit moet nog gechecked worden
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game
        previousHintType = 'None'

    def on_press(self):
        self.pressed = True
    
    def on_release(self):
        if self.pressed:
            getHintOutput = functions.getHint(api.get_character(), previousHintType) #Dataset moet zegmaar de data uit de api zijn met {'name':iron,'desc':{description:'', comics:[], films:[]}
            previousHintType = getHintOutput[1]                            #Dit moet uitgevoerd worden wanneer op de knop gedrukt wordt
            hint = getHintOutput[0]                                        #Eventueel moet ook points() er nog bij maar idunno -Rick
            currentPoints = functions.points()
'''


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
        arcade.draw_text(self.character, self.center_x, self.center_y, arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")

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
        arcade.draw_text(self.text, self.center_x, self.center_y, arcade.color.BLACK, align="center", anchor_x="center", anchor_y="center")

class Cursor(arcade.Sprite):
    '''invisable cursor as long you dont draw'''
    def __init__(self, x, y, sprite):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite)
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
        self.test = api.get_character()['name']
        print(type(self.test))
        self.timer = int()
        self.delta_timer = float()
        self.score = int()
        self.characterList = []

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
            for button in self.possible_answer_buttons:
                button.draw()
                button.draw_text()
        elif self.state == State.hard:
            pass
        elif self.state == State.leaderboard:
            pass
    
    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second. """
        self.delta_timer += delta_time
        if self.delta_timer >= 1:
            self.timer += 1
            self.delta_timer = 0

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if self.state == State.title_screen:
            print(modifiers)
            print('pass')
            if key != arcade.key.BACKSPACE and chr(key).lower() in 'abcdefghijklmnopqrstuvwxyz1234567890' and len(self.name) < 10: #geen back space en filter
                print('nieuw letter')
                if modifiers == 17 or modifiers == 1: #shift voor hoofdletter
                    self.name += str(chr(key)).upper()
                else:
                    print(self.name)
                    self.name += str(chr(key))
            elif key == arcade.key.BACKSPACE:
                self.name = self.name[:-1]

    def on_key_release(self, key, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.center_x = x
        self.cursor.center_y = y 

    def on_mouse_release(self, x, y, button, modifiers):
        print(button)
        if self.state == State.mode:
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.mode_buttons)
            for button in cursor_collides_with:
                self.state = button.state
        elif self.state == State.title_screen:
            if arcade.check_for_collision(self.cursor, self.submit_name_button) and len(self.name) >= 3:
                self.state = self.submit_name_button.state
        elif self.state == State.choose_difficulty:
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.difficulty_buttons)
            for button in cursor_collides_with:
                self.state = button.state
                if button.state == State.easy:
                    self.correctCharacter = api.get_character(True)
                    self.characterList.append(self.correctCharacter['name'])
                    for i in range(0, 9):
                        self.character = api.get_character()
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
                            self.possible_answer_buttons.append(CharacterButton(WINDOW_WIDTH/8, WINDOW_HEIGHT/6 * (self.characterList.index(index) + 1), 'Button.png', index))
                        else:
                            self.possible_answer_buttons.append(CharacterButton(WINDOW_WIDTH/8*7, WINDOW_HEIGHT/6 * (self.characterList.index(index) - 4), 'Button.png', index))



def main():
    """ Create an instance of our game window and start the Arcade game loop. """
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()

# only start the game if this script is executed as the main process
if __name__ == "__main__":
    main()