from random import seed, random
from math import *

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
        self.str_mod = 0
        self.dex_mod = 0
        self.con_mod = 0
        self.int_mod = 0
        self.wis_mod = 0
        self.char_mod = 0

    # Strength modifier
    @property
    def str_mod(self):
        return self._str_mod
    @str_mod.setter
    def str_mod(self, val):
        self._str_mod = val
    
    #Dexterity modifier
    @property
    def dex_mod(self):
        return self._dex_mod
    @dex_mod.setter
    def dex_mod(self, val):
        self._dex_mod = val
    
    #Constitution modifier
    @property
    def con_mod(self):
        return self._con_mod
    @con_mod.setter
    def con_mod(self, val):
        self._con_mod = val
    
    #Intelligence modifier
    @property
    def int_mod(self):
        return self._int_mod
    @int_mod.setter
    def int_mod(self, val):
        self._int_mod = val
    
    #Wisdom modifier
    @property
    def wis_mod(self):
        return self._wis_mod
    @wis_mod.setter
    def wis_mod(self, val):
        self._wis_mod = val
    
    #Charisma modifier
    @property
    def char_mod(self):
        return self._char_mod
    @char_mod.setter
    def char_mod(self, val):
        self._char_mod = val
    

    #Creates a dictionary to connect every modifier to their respective values. 
    #Allows interchangability in the modifiers and stats, a "one function for all" in a sense.
    def set_mod(self, modifier, value):
        list = {"str":self._str_mod, "dex":self._dex_mod, "con":self._con_mod, "int":self._int_mod, "wis":self._wis_mod, "char":self._char_mod}
        list[modifier] += self.mod(value)
        return list[modifier]



    #Modifiers are assigned their values based on a 50/50 split system, values below 10 become negative, values above 11 become positive.
    #Its possible to have stats as high as 30, but the values would work all the same and for simplicity sake I ignored it (Its uncommon).
    def mod(self, modifier):
     lower_half =  [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
     upper_half = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
     if (modifier in lower_half):
        return floor((lower_half.index(modifier) / 2) * (-1))
     if (modifier in upper_half):
        return trunc(((upper_half.index(modifier)+1)  / 2) * (1))

    @property
    def side(self): 
        return self._side
    
    # Checks if inputed value is below 1 and sets it to 1. Otherwise takes inputed value. 
    @side.setter
    def side(self, value): 
        if (value < 4): 
            self._side = 4
        elif (value >= 4): 
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
    # Added a dictionary to choose which modifier to add to the roll. Intended for a button / switch system, can be changed.
    def roll_dice(self, modifier): 
        list = {"str":self._str_mod, "dex":self._dex_mod, "con":self._con_mod, "int":self._int_mod, "wis":self._wis_mod, "char":self._char_mod}
        dice_roll = 0
        for x in range(self.qty):
            seed()
            dice_roll += (int(random()*self._side + 1) + list[modifier])
        return f"{dice_roll}"
    
    def modded_diceRoll(self):
        pass
    
    def __str__(self): 
        return f"This rolls a {self.side} sided dice {self.qty} time(s)."
    
    # The return statements for roll_dice() and __str__() can be changed in the future. 
    # Needs to be able to include stat modifiers in the rolls. Cole can help with that. 

    # Note: All values have an underscore because it runs into an infinite recursion
    # loop if it doesn't. If anyone wants to fix it to make it "cleaner", they can do so
    # themselves. 

# For testing: 
d20 = Dice()
d8 = Dice(8)
d4 = Dice(4, 2)


print(d20.roll_dice("str"))
print(d8)
print(d4.roll_dice("str"))
print(d20.set_mod("str", 20))
print(d20.roll_dice("str"))



