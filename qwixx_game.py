import tkinter as gui
import random as rng

class Window(gui.Tk):
    # Construct GUI
    def __init__(self, parent):
        gui.Tk.__init__(self, parent)
        self.parent = parent
        self.draw_window()
        
        self.game = Qwixx()
        
    def draw_window(self):
        # Paths to dice images
        #self.green_dice = []
        #self.blue_dice = []
        #self.yellow_dice = []
        #self.red_dice = []
        
        self.white_dice = [gui.PhotoImage(file="images/die1.png"), 
                gui.PhotoImage(file="images/die2.png"),
                gui.PhotoImage(file="images/die3.png"), 
                gui.PhotoImage(file="images/die4.png"),
                gui.PhotoImage(file="images/die5.png"), 
                gui.PhotoImage(file="images/die6.png")]
        
        # Resize the images by sampling large image
        self.resize = [self.white_dice[0].subsample(6, 6), 
                self.white_dice[1].subsample(6, 6), 
                self.white_dice[2].subsample(6, 6),
                self.white_dice[3].subsample(6, 6), 
                self.white_dice[4].subsample(6, 6), 
                self.white_dice[5].subsample(6, 6)]
        
        # Define the dice frame
        self.dice_frame = gui.Frame(self, width=1000, height=150)
        self.dice_frame.pack()
        self.button_frame = gui.Frame()
        # Define the reroll button and the command it should call
        gui.Button(self, text="Next Roll", command=self.on_button_click).pack()
        gui.Button(self, text="Remove Red Die", command=self.on_button_click).pack()
        gui.Button(self, text="Remove Green Die", command=self.on_button_click).pack()
        gui.Button(self, text="Remove Blue Die", command=self.on_button_click).pack()
        gui.Button(self, text="Remove Yellow Die", command=self.on_button_click).pack()
    
    def on_button_click(self):
        # Empty the window
        for x in self.dice_frame.winfo_children():
            x.destroy()
        
        # Grab the dice rolls and draw them on the board
        rolls = self.game.request_roll()
        for colour in rolls:
            gui.Label(self.dice_frame, image=self.resize[rolls[colour]]).pack(side=gui.LEFT)


class Qwixx():
    # Define the six coloured dice present in a Qwixx game
    qwixx_dice = {"white_1": 0, "white_2": 0, "red": 0,
                "blue": 0, "green": 0, "yellow": 0}
    
    # Roll each of the dice present in the game
    def request_roll(self):
        for die in self.qwixx_dice:
            self.qwixx_dice[die] = rng.randint(0, 5)
        return self.qwixx_dice
    
    # Remove a colour from the game
    def remove_die(self, colour):
        if qwixx_dice.has_key(colour):
            qwixx_dice.pop(colour)
        else:
            print("Die colour has already been removed.")

if __name__ == "__main__":
    app = Window(None)
    app.title("Qwixx Dice Roller")
    app.mainloop()
