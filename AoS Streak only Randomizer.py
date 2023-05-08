'''
1. Randomizer Logic
    1. Map Generation (!)
    2. Embarkation Clone
    3. Forsaken Altar (!)
2. JSON manip (!)
3. GUI
    1. Foundation (!)
    2. Caravan
    3. Beautify
4. Alt Options
'''

import tkinter as tk
from tkinter import ttk
import json
import random

# def select():
#     if var.get() == 1:
#         word = "Streaker's Preset"
#     selection = 'You selected the option ' + word
#     label.config(text = selection)



def getsave(): #fetches the file; still need to change the filepath to be "universal"
    with open('C:/Users/kevin/AppData/LocalLow/Eremite Games/Against the Storm/CustomGamesLayout.save', 'r') as file:
        gsdata = json.load(file)
    print('got save')
    return gsdata

def overwritesave(owsdata, prestige_var, altar_var):    #set the variables in the save file object, and then save it again. 
    i = 1
    while i < 6:        
        owsdata['layouts'][i]['name'] = str(i) + 'John'
        settingslist = randomize(prestige_var, altar_var)
        owsdata['layouts'][i]['seed'] = settingslist[1]
        owsdata['layouts'][i]['biome'] = settingslist[0]
        owsdata['layouts'][i]['modifiers'] = settingslist[2]
        setperma(owsdata, i)
        i += 1


    # Save updated JSON back to file
    with open('C:/Users/kevin/AppData/LocalLow/Eremite Games/Against the Storm/CustomGamesLayout.save', 'w') as file:
        json.dump(owsdata, file, indent=4)
    print("JSON data updated and saved successfully.")


def randomize(prestige_var, altar_var):    #The first section of randomizing the save
    rng = random.SystemRandom().randint(1,1000000000)
    biome = (rng % 5)
    mods = modgen(rng, prestige_var, altar_var) #this particular function invoked is where RNG decides which modifiers to include
    match biome:
        case 0:
            biome = 'Royal Woodlands'
        case 1:
            biome = 'Coral Forest'
        case 2:
            biome = 'Cursed Royal Woodlands'
        case 3:
            biome = 'Scarlet Orchard'
        case 4:
            biome = 'The Marshlands'

    seed = random.SystemRandom().randint(1,99999999)
    return [biome, seed, mods]


def modgen(rng, prestige_var, altar_var): #decides the number of mods to enabled, and what the odds are. 
    #Out of 100 games; 15 will have no modifiers, 20 will have 1 positive, 20 will have 1 Negative, 20 will have 1 of each, 4 will have 1 positive and two negative
    #3 will have 2 positives and 1 negative, 7 will have two of each, 7 Will have two positive, and 3 will have two negatives.
    #The above is intended to be edited significantly after some trial runs with other P20 players. 
    rng = rng % 100
    if rng in range(0,15): #Python's trailing number in a range is not inclusive
        return []
    elif rng in range (15,35):
        return modselect(1,0,prestige_var, altar_var)
    elif rng in range (35,55):
        return modselect(0,1,prestige_var, altar_var)
    elif rng in range (55,75):
        return modselect(1,1,prestige_var, altar_var)
    elif rng in range (75,79):
        return modselect(1,2,prestige_var, altar_var)
    elif rng in range (79,82):
        return modselect(2,1,prestige_var, altar_var)
    elif rng in range (82,89):
        return modselect(2,2,prestige_var, altar_var)
    elif rng in range (89,96):
        return modselect(2,0,prestige_var, altar_var)    
    elif rng in range (96,100):
        return modselect(0,2,prestige_var, altar_var)
    else:
        print('Error when deciding mod count')


def modselect(x: int, y: int, prestige_var, altar_var): #This is where we actually pick the lucky mods that the player gets to benefit or suffer from
    modselected = []
    poslist = ["[Map Mod] 3 Order Picks", "[Mod] Replace Initial Glade - Ruins", "ModifierEffect_AdditionalGrass", "[Map Mod] Hostility People", "[Map Mod] Move", "[Map Mod] No Hostility", "[Map Mod] Bonus Timed Orders", "[Map Mod] Overgrown Library", "[Map Mod] Petrified Necropolis", "[Map Mod] Ruins", "[Map Mod] Trader Attack"]
    neglist = ["ModifierEffect_TradeBlock_Composite", "ModifierEffect_NoGrass", "[Map Mod] Dangerous Lands", "[Map Mod] Forbidden Lands", "[Mod] Less Hearth Range", "[Mod] Gathering Storm", "[Map Mod] Initial Hostility", "[Map Mod] Initial Impatience", "[Mod] Land of Greed", "[Map Mod] No Control", "[Map Mod] No Glade Info", "[Map Mod] No Goods Refund", "[Map Mod] No Orders", "[Mod] Ominous Presence", "[Map Mod] One Perk", "Pause Block", "ModifierEffect_TreeCuttingTime", "[Map Mod] Untamed Wilds", "ModifierEffect_LongStorm"]
    numofpositive = 11 - 1 #keep -1 in place to avoid off by one errors, left number is the number of mods in the game that is included in this. 
    numofnegative = 19 - 1
    pos1 = random.SystemRandom().randint(1,numofpositive)
    pos2 = pos1
    while pos2 == pos1:
        pos2 = random.SystemRandom().randint(1,numofpositive) #this loop ensures that the second positive mod is different from the first
    neg1 = random.SystemRandom().randint(1,numofnegative)
    neg2 = neg1
    while neg2 == neg1:
        neg2 = random.SystemRandom().randint(1,numofnegative)
    if x == 0:
        pass
    elif x == 1:
        modselected.append(poslist[pos1])
    elif x == 2:
        modselected.append(poslist[pos1])
        modselected.append(poslist[pos2])
    else:
        print('Error when adding positive mods')
    if y == 0:
        pass
    elif y == 1:
        modselected.append(neglist[neg1])
    elif y == 2:
        modselected.append(neglist[neg1])
        modselected.append(neglist[neg2])
    else:
        print('Error when adding negative mods')
    if altar_var == True:
        modselected.append('[Diff] Altar')
    if prestige_var == True:
        P20List = ["[Mod] Higher Blueprints Reroll Cost", "[Mod] Faster Leaving", "[Mod] Wet Soil", "[Mod] Parasites", "[Mod] Higher Needs Consumption Rate", "[Mod] Longer Relics Working Time", "[Mod] Higher Traders Prices", "[Mod] Fewer Blueprints Options", "[Mod] Fewer Cornerstones Options", "[Mod] Lower Impatience Reduction", "[Mod] Longer Storm", "[Mod] Fewer Initial Blueprints", "[Diff] Hunger Multiplier", "[Mod] Faster Fuel Sacrafice", "[Mod] Exploration Tax", "[Mod] Additional Impatience for Death"]
        for each in P20List:
            modselected.append(each)

    return modselected

def setperma(owsdata, i):
    #tradeTowns - might not work this way; we'll see! Be sure to test this a bit more throughly once we get to testing stage
    #Town 1
    owsdata['layouts'][i]['tradeTowns'][0]['x'] = 1
    owsdata['layouts'][i]['tradeTowns'][0]['y'] = -8
    owsdata['layouts'][i]['tradeTowns'][0]['z'] = 7
    owsdata['layouts'][i]['tradeTowns'][0]['magnitude'] = 10.6770782
    owsdata['layouts'][i]['tradeTowns'][0]['sqrMagnitude'] = 114
    #Town 2
    owsdata['layouts'][i]['tradeTowns'][1]['x'] = -8
    owsdata['layouts'][i]['tradeTowns'][1]['y'] = 6
    owsdata['layouts'][i]['tradeTowns'][1]['z'] = 2
    owsdata['layouts'][i]['tradeTowns'][1]['magnitude'] = 10.1980391
    owsdata['layouts'][i]['tradeTowns'][1]['sqrMagnitude'] = 104
    #Town 3
    owsdata['layouts'][i]['tradeTowns'][2]['x'] = -8
    owsdata['layouts'][i]['tradeTowns'][2]['y'] = -1
    owsdata['layouts'][i]['tradeTowns'][2]['z'] = 9
    owsdata['layouts'][i]['tradeTowns'][2]['magnitude'] = 12.083046
    owsdata['layouts'][i]['tradeTowns'][2]['sqrMagnitude'] = 146
    #City
    owsdata['layouts'][i]['tradeTowns'][3]['x'] = 0
    owsdata['layouts'][i]['tradeTowns'][3]['y'] = 0
    owsdata['layouts'][i]['tradeTowns'][3]['z'] = 0
    owsdata['layouts'][i]['tradeTowns'][3]['magnitude'] = 0.0
    owsdata['layouts'][i]['tradeTowns'][3]['sqrMagnitude'] = 0
    #Everything Else
    owsdata['layouts'][i]['difficultyIndex'] = 3
    owsdata['layouts'][i]['isBlightActive'] = True
    owsdata['layouts'][i]['blightFootprintIndex'] = 1
    owsdata['layouts'][i]['reputationIndex'] = 1
    owsdata['layouts'][i]['reputationPenaltyIndex'] = 3
    owsdata['layouts'][i]['reputationPenaltyRateIndex'] = 1
    owsdata['layouts'][i]['positiveSeasonalEffectsAmount'] = 1
    owsdata['layouts'][i]['negativeSeasonalEffectsAmount'] = 4

class Window(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.title('Window')
        self.geometry("250x150")
        #self.resizable(False,False)
        self.create_widgets()

    def create_widgets(self):
        self.prestige_var = tk.BooleanVar()
        self.altar_var = tk.BooleanVar()

        prestige_checkbox = ttk.Checkbutton(self, text="Prestige?", variable=self.prestige_var)
        prestige_checkbox.pack(pady=10)

        altar_checkbox = ttk.Checkbutton(self, text="Altar?", variable=self.altar_var)
        altar_checkbox.pack()

        ok_button = ttk.Button(self, text="OK", command=self.on_ok_button_click)
        ok_button.pack(pady=10)

    def on_ok_button_click(self):
        prestige_state = self.prestige_var.get()
        altar_state = self.altar_var.get()
        data = getsave()
        overwritesave(data, prestige_state, altar_state)
        self.destroy()


if __name__ == "__main__":
    window = Window()
    window.mainloop()


