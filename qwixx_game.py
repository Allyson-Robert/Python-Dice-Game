import tkinter as gui
import random as rng

IMAGE_PATH="images/{}/die{}.png"
SIDES = 6

WHITE="#cbcbcb"
YELLOW="#ffff00"
RED="#ff0000"
GREEN="#007c00"
BLUE="#3137ff"
BLACK="#000000"

class Window(gui.Tk):
    # Construct GUI
    def __init__(self, parent):
        # tkinter initialisation
        gui.Tk.__init__(self, parent)
        self.parent = parent
        
        # General settings
        self.title("Qwixx Dice Roller")
        self.geometry("1150x250")
        
        self.initialise()
        
        # Hold the window open
        self.mainloop()
    
    def initialise(self):
        # Initialise Game
        self.game = Qwixx()
        self.game_state = "initial"
        
        # Generate a list of appropriately sized images
        self.dice_images = self.game.request_dice()
        for colour in self.dice_images:
            self.dice_images[colour] = []
            name = colour if not "white" in colour else "white" 
            for face in range(SIDES + 1):
                image_reference = gui.PhotoImage(file=IMAGE_PATH.format(name, face))
                self.dice_images[colour] += [image_reference.subsample(3, 3)]
        
        # Initialise window and game
        self.draw_window()
        
        # Event handling/Button binding
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<space>', lambda e: self.button_next_roll())
        self.bind('<Return>', lambda e: self.on_restart())
        self.bind('q', lambda e: self.destroy())
    
    def draw_window(self):
        # Define the dice frame
        self.dice_frame = gui.Frame(self, width=1000, height=200)
        self.dice_frame.pack(side=gui.TOP)
        
        # Draw initialised dice (empty dice)
        self.update_dice(self.game.request_dice())
        
        # Define the button frame
        self.button_frame = gui.Frame()
        self.button_frame.pack(side=gui.BOTTOM)
        
        # Define the buttons and the command they should call
        self.next_roll_button = gui.Button(self, text="Next Roll (Space)", 
                command=self.button_next_roll)
        self.rmv_y_button = gui.Button(self, text="Remove Yellow Die", bg=YELLOW, fg='black', 
                command=lambda: self.remove_colour("yellow"))
        self.rmv_r_button = gui.Button(self, text="Remove Red Die", bg=RED, fg='black', 
                command=lambda: self.remove_colour("red"))
        self.rmv_g_button = gui.Button(self, text="Remove Green Die", bg=GREEN, fg='black', 
                command=lambda: self.remove_colour("green"))
        self.rmv_b_button = gui.Button(self, text="Remove Blue Die", bg=BLUE, fg='white', 
                command=lambda: self.remove_colour("blue"))
        
        # Disable the removal buttons until the first roll
        self.rmv_y_button.config(state="disabled")
        self.rmv_r_button.config(state="disabled")
        self.rmv_g_button.config(state="disabled")
        self.rmv_b_button.config(state="disabled")
            
        # Position buttons adjacent to eachother from left to right
        self.next_roll_button.pack(in_=self.button_frame, side=gui.LEFT)
        self.rmv_y_button.pack(in_=self.button_frame, side=gui.LEFT)
        self.rmv_r_button.pack(in_=self.button_frame, side=gui.LEFT)
        self.rmv_g_button.pack(in_=self.button_frame, side=gui.LEFT)
        self.rmv_b_button.pack(in_=self.button_frame, side=gui.LEFT)
        
    def button_next_roll(self):
        # Grab the dice rolls and draw them on the board
        rolls = self.game.request_roll()
        self.update_dice(rolls)
        
        # Enable removal buttons after the first roll
        if self.game_state == "initial":
            self.game_state = "ongoing"
            self.rmv_y_button.config(state="active", bg=YELLOW, fg='black')
            self.rmv_r_button.config(state="active", bg=RED, fg='black')
            self.rmv_g_button.config(state="active", bg=GREEN, fg='black')
            self.rmv_b_button.config(state="active", bg=BLUE, fg='white')
    
    def update_dice(self, dice_rolls):
        # Empty the window
        for x in self.dice_frame.winfo_children():
            x.destroy()
        
        # Place the dice
        for colour in dice_rolls:
            face = dice_rolls[colour]
            image_to_show = self.dice_images[colour][face]
            gui.Label(self.dice_frame, image=image_to_show).pack(side=gui.LEFT)

    def remove_colour(self, colour):
        self.game_state = self.game.rmv_die(colour)
        self.disable_button(colour)
        self.update_dice(self.game.request_dice())
        self.check_state()
    
    def disable_button(self, colour):
        if colour == "yellow":
            self.rmv_y_button.config(state="disabled")
        elif colour == "red":
            self.rmv_r_button.config(state="disabled")
        elif colour == "green":
            self.rmv_g_button.config(state="disabled")
        else : 
            self.rmv_b_button.config(state="disabled")
    
    def check_state(self):
        if self.game_state != "game_over":
            return 0
        
        # Empty the window
        self.dice_frame.destroy()
        self.button_frame.destroy()
        
        # Show "Game Over" message
        self.end_frame= gui.Frame(self, width=1000, height=200)
        self.end_frame.pack(side=gui.TOP)
        self.game_over_label = gui.Label(self.end_frame, text="Game Over!", 
                font=("Helvetica", 64))
        self.game_over_label.pack(side=gui.LEFT)
        
        # Add a restart button
        self.restart_button = gui.Button(self, text="Restart? (Return)",  command=self.on_restart)
        self.restart_button.pack()
        
    def on_restart(self):
        # Remove end screen and initialise game again
        self.end_frame.destroy()
        self.game_over_label.destroy()
        self.restart_button.destroy()
        self.initialise()

class Qwixx():
    # Define the six coloured dice present in a Qwixx game
    def __init__(self):
        self.qwixx_dice = {"white_1": 0, "white_2": 0, "yellow": 0, 
            "red": 0, "green": 0, "blue": 0}
    
    def reset_dice(self):
        for die in self.qwixx_dice:
            self.qwixx_dice[die] = 0
    
    # Request dice
    def request_dice(self):
        return self.qwixx_dice.copy()
    
    # Roll each of the dice present in the game
    def request_roll(self):
        for die in self.qwixx_dice:
            self.qwixx_dice[die] = rng.randint(1, 6)
        return self.qwixx_dice.copy()
    
    # Remove a colour from the game, set state to game_over if second dice has been removed
    def rmv_die(self, colour):
        self.qwixx_dice.pop(colour)
        self.reset_dice()
        
        if len(self.qwixx_dice) < 5:
            return "game_over"
        return "ongoing"

if __name__ == "__main__":
    app = Window(None)
