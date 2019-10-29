import arcade
from enum import Enum
import functions
import api


# Set up the constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Marvel"
WINDOW_BACKGROUND_COLOR = arcade.color.BLACK

class State(Enum):
    title_screen = 0
    mode = 1
    easy = 2
    hard = 3
    leaderboard = 4

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


class StateButton(arcade.Sprite):
    '''
    a button that changes the state
    '''
    def __init__(self, x, y, sprite, state):
        super().__init__()
        self.sprite = sprite
        self.texture = arcade.load_texture(self.sprite)
        self.center_x = x
        self.center_y = y
        self.state = state

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
        self.background = Background(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 'iron man startscherm-1.png.png')
        self.state = State.title_screen
        self.name = str()
        self.mode_buttons = arcade.SpriteList()
        self.mode_buttons.append(StateButton(300, 400, 'Button.png', State.easy))
        self.cursor = Cursor(0, 0, 'Wrong.png')

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        #on_draw funcite voor alle verschillende menu's
        arcade.start_render()
        self.background.draw()
        if self.state == State.title_screen:
            arcade.draw_text(self.name, WINDOW_WIDTH/2,WINDOW_HEIGHT/2,arcade.color.BLACK, 36, bold=True)
        elif self.state == State.mode:
            for button in self.mode_buttons:
                button.draw()
        elif self.state == State.easy:
            pass
        elif self.state == State.hard:
            pass
        elif self.state == State.leaderboard:
            pass
    
    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second. """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if self.state == State.title_screen:
            print('pass')
            if key != arcade.key.BACKSPACE and chr(key).lower() in 'abcdefghijklmnopqrstuvwxyz': #geen back space en filter
                print('nieuw letter')
                if modifiers == 17: #shift voor hoofdletter
                    self.name += str(chr(key)).upper()
                else:
                    print(self.name)
                    self.name += str(chr(key))
                    print(self.name)
            elif key == arcade.key.BACKSPACE:
                print('minus')
                self.name = self.name[:-1]
            elif key == arcade.key.ENTER and len(self.name) >= 3:
                self.state = State.mode

    def on_key_release(self, key, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.x = x
        self.cursor.y = y 

    def on_mouse_release(self, x, y, button, modifiers):
        print(button)
        if self.state == State.mode:
            cursor_collides_with = arcade.check_for_collision_with_list(self.cursor, self.mode_buttons)
            for button in cursor_collides_with:
                self.state = button.state

def main():
    """ Create an instance of our game window and start the Arcade game loop. """
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()

# only start the game if this script is executed as the main process
if __name__ == "__main__":
    main()