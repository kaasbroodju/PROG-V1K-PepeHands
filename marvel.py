import arcade
import functions


# Set up the constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Marvel"
WINDOW_BACKGROUND_COLOR = arcade.color.BLACK

class hintButton(Textbutton):
    def __init__ (self, game, x=0, y=0, width=100, height=40, text="`Hint`", theme=None): #Dit moet nog gechecked worden
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game
        previousHintType = 'None'

    def on_press(self):
        self.pressed = True
    
    def on_release(self):
        if self.pressed:
            getHintOutput = functions.getHint(?dataset?, previousHintType) #Dataset moet zegmaar de data uit de api zijn met {'name':iron,'desc':{description:'', comics:[], films:[]}
            previousHintType = getHintOutput[1]                            #Dit moet uitgevoerd worden wanneer op de knop gedrukt wordt
            hint = getHintOutput[0]                                        #Eventueel moet ook points() er nog bij maar idunno -Rick

        


class MyGame(arcade.Window):
    """ An Arcade game. """
    def __init__(self, width, height, title):
        """ Constructor. """
        super().__init__(width, height, title, resizable=True)
        arcade.set_background_color(WINDOW_BACKGROUND_COLOR)

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        #on_draw funcite voor alle verschillende menu's
        arcade.start_render()
    
    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second. """
        pass

def main():
    """ Create an instance of our game window and start the Arcade game loop. """
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    arcade.run()

# only start the game if this script is executed as the main process
if __name__ == "__main__":
    main()