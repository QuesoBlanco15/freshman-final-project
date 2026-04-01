from random import seed, random

# An easily adjustable dice class that can take number of sides and how many die
# being rolled. Includes a roll_dice() function and __str__() function. 
class Dice(): 
    # __init__() takes number of sides and number of die. Defaults to 20 and 1 respectively.
    # Included stats and stats_mod lists for future additions.  
    def __init__(self, side=20, qty=1): 
        self.side = side
        self.qty = qty
        self.stats = []
        self.stats_mod = []

    @property
    def side(self): 
        return self._side
    
    # Checks if inputed value is below 1 and sets it to 1. Otherwise takes inputed value. 
    @side.setter
    def side(self, value): 
        if (value < 1): 
            self._side = 1
        elif (value >= 1): 
            self._side = value
        else: 
            self._side = 20
    
    @property
    def qty(self): 
        return self._qty
    
    # Checks if inputed value is below 1 and sets it to 1. Otherwise takes inputed value. 
    @qty.setter
    def qty(self, value): 
        if (value < 1): 
            self._qty = 1
        else: 
            self._qty = value
    
    # Similar to previous function except can specify number of times rolled. 
    # In the future, can include stat modifiers or show each dice roll in a 
    # returned list instead of just the total added up. 
    def roll_dice(self): 
        dice_roll = 0
        for x in range(self._qty):
            seed()
            dice_roll += int(random()*self._side + 1)
        return f"Rolled {self._qty} times added up to {dice_roll} total."
    
    def __str__(self): 
        return f"This rolls a {self._side} sided dice {self._qty} time(s)."
    
    # The return statements for roll_dice() and __str__() can be changed in the future. 
    # Needs to be able to include stat modifiers in the rolls. Cole can help with that. 

    # Note: All values have an underscore because it runs into an infinite recursion
    # loop if it doesn't. If anyone wants to fix it to make it "cleaner", they can do so
    # themselves. 

# For testing: 
d20 = Dice()
d8 = Dice(8)
d4 = Dice(4, 2)

print(d20.roll_dice())
print(d8)
print(d4.roll_dice())
