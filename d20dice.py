# This is just a basic test on how to make each dice roll random. Can be improved upon or
# changed depending on future needs. - AF

from random import seed, random

# Each time this is called, it will make a new seed and use that seed to return 
# a dice roll from 1-20. By default, the seed is generated based on the current
# system time. 
def roll_dice(type):
     seed()
     dice_roll = int(random()*type + 1)
     return dice_roll
      
# May run into a problem if, for example, each session is played around the same 
# time, resulting in similar rolls. Can add more random factors to increase rng. - AF

# I don't exactly know how advantage rolls work with stats. Cole has to explain or 
# integrate that himself. - AF

