import tkinter as gui
import random as rng

class Window(gui.Tk):
    # Construct GUI
    def __init__(self, parent):
        gui.Tk.__init__(self, parent)
        self.parent = parent
        self.game = Qwixx()
        self.draw_window()
        
    def draw_window(self):
        # Paths to dice images
        #self.green_dice = []
        #self.blue_dice = []
        #self.yellow_dice = []
        #self.red_dice = []
        
        self.white_dice = [gui.PhotoImage(file="images/yellow/die0.png"),
                gui.PhotoImage(file="images/yellow/die1.png"), 
                gui.PhotoImage(file="images/yellow/die2.png"),
                gui.PhotoImage(file="images/yellow/die3.png"), 
                gui.PhotoImage(file="images/yellow/die4.png"),
                gui.PhotoImage(file="images/yellow/die5.png"), 
                gui.PhotoImage(file="images/yellow/die6.png")]
        
        # Resize the images by sampling large image
        self.resize = [self.white_dice[0].subsample(3, 3), 
                self.white_dice[1].subsample(3, 3), 
                self.white_dice[2].subsample(3, 3), 
                self.white_dice[3].subsample(3, 3),
                self.white_dice[4].subsample(3, 3), 
                self.white_dice[5].subsample(3, 3), 
                self.white_dice[6].subsample(3, 3)]
        
        # Define the dice frame
        self.dice_frame = gui.Frame(self, width=1068, height=178)
        self.dice_frame.pack(side=gui.TOP)
        
        dice = self.game.request_dice()
        self.update_dice(dice)
        
        # Define the button frame
        self.button_frame = gui.Frame()
        self.button_frame.pack(side=gui.BOTTOM)
        
        # Define the reroll button and the command it should call
        next_roll_button = gui.Button(self, text="Next Roll", command=self.button_next_roll)
        remove_r_button = gui.Button(self, text="Remove Red Die", command=self.button_remove_r)
        remove_g_button = gui.Button(self, text="Remove Green Die", command=self.button_remove_g)
        remove_b_button = gui.Button(self, text="Remove Blue Die", command=self.button_remove_b)
        remove_y_button = gui.Button(self, text="Remove Yellow Die", command=self.button_remove_y)
        
        next_roll_button.pack(in_=self.button_frame, side=gui.LEFT)
        remove_r_button.pack(in_=self.button_frame, side=gui.LEFT)
        remove_g_button.pack(in_=self.button_frame, side=gui.LEFT)
        remove_b_button.pack(in_=self.button_frame, side=gui.LEFT)
        remove_y_button.pack(in_=self.button_frame, side=gui.LEFT)
    
    def button_next_roll(self):
        # Empty the window
        for x in self.dice_frame.winfo_children():
            x.destroy()
        
        # Grab the dice rolls and draw them on the board
        rolls = self.game.request_roll()
        self.update_dice(rolls)
    
    def update_dice(self, dice_rolls):
        for colour in dice_rolls:
            gui.Label(self.dice_frame, image=self.resize[dice_rolls[colour]]).pack(side=gui.LEFT)
        print(self.dice_frame.winfo_width(), self.dice_frame.winfo_height())
    
    def button_remove_r(self):
        self.game.remove_die("red")
    
    def button_remove_g(self):
        self.game.remove_die("green")
    
    def button_remove_b(self):
        self.game.remove_die("blue")
    
    def button_remove_y(self):
        self.game.remove_die("yellow")
    
class Qwixx():
    # Define the six coloured dice present in a Qwixx game
    qwixx_dice = {"white_1": 0, "white_2": 0, "red": 0,
                "blue": 0, "green": 0, "yellow": 0}
    
    # Request dice
    def request_dice(self):
        return self.qwixx_dice
    
    # Roll each of the dice present in the game
    def request_roll(self):
        for die in self.qwixx_dice:
            self.qwixx_dice[die] = rng.randint(1, 6)
        return self.qwixx_dice
    
    # Remove a colour from the game
    def remove_die(self, colour):
        if colour in self.qwixx_dice:
            self.qwixx_dice.pop(colour)
            print(colour.capitalize(), "die has been removed.")
        else:
            print("Die colour has already been removed previously.")
        if len(self.qwixx_dice) < 5:
            print("Game Over!")

if __name__ == "__main__":
    app = Window(None)
    app.title("Qwixx Dice Roller")
    app.mainloop()
