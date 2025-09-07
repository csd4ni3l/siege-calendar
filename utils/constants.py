import re

HACKATIME_URL = "https://hackatime.hackclub.com/api/v1"

LOGO_ASCII_ART = """
   _____ _                    _____      _                _            
  / ____(_)                  / ____|    | |              | |           
 | (___  _  ___  __ _  ___  | |     __ _| | ___ _ __   __| | __ _ _ __ 
  \___ \| |/ _ \/ _` |/ _ \ | |    / _` | |/ _ \ '_ \ / _` |/ _` | '__|
  ____) | |  __/ (_| |  __/ | |___| (_| | |  __/ | | | (_| | (_| | |   
 |_____/|_|\___|\__, |\___|  \_____\__,_|_|\___|_| |_|\__,_|\__,_|_|   
                 __/ |                                                 
                |___/      
"""

PROJECT_INFO = """
Project by csd4ni3l made for Hack Club Siege!
Website: https://csd4ni3l.hu
Github: https://github.com/csd4ni3l/siege-calendar"""

HOME_SCREEN = """
Welcome to Siege Calendar, please press one of the following keys to interact!
It's currently {siege_week}! Siege that castle, or else...

t - Today's Coding Stats
a - All Time Coding Stats
p - Projects
h - Shop
g - Goals
s - Statistics
c - Calendar
q - Quit"""

GOALS_SCREEN = """
Welcome to the Goals section, please press one of the following keys to interact!
a - Add Goal
r - Remove Goal
q - Quit

Your current goals are:
{goals}
"""

SHOP_SCREEN = """
Welcome to the Shop, please add your bought items here, so the program knows of it!

Available items:
"""

shop_items = [
    ["Mercenaries", "Saves you 1 hour from the current week", 15, 9999],
    ["8 GB RAM Upgrade", "Up to 7, stacks", 75, 7],
    ["SSD upgrade 1TB", "Can be bought once", 100, 1],
    ["SSD upgrade 2TB", "Can be bought once",  150, 1],
    ["CPU Upgrade", "to i5-1334U", 300, 1],
    ["FW 13 Upgrade", "CPU needs to be bought first", 150, 1]
]