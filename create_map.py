from pymongo import MongoClient
import random
import os

client = MongoClient()
db = client.map


def create_map(len_x,len_y):
    os.system('clear')
    for i in range(len_y):
        for g in range(len_y):
            x,y = g,i
            NATURE_LEVEL = random.randrange(1,10)
            PRESSURE = random.randrange(1,10)
            MANA_GOLD = random.randrange(51,95)/100
            MANA_SHIT = 1 - MANA_GOLD
            REGENERATION = random.randrange(1,10)
            CAPACITY_LEVEL = random.randrange(10,1000)
            player_id = 0000
            people = 100
            shit = 0
            capacity = CAPACITY_LEVEL
            nature = random.randrange(1,10)
            
            cell = {'x':x,'y':y,'NATURE_LEVEL':NATURE_LEVEL,'PRESSURE':PRESSURE,
                    'MANA_GOLD':MANA_GOLD,'MANA_SHIT':MANA_SHIT,'REGENERATION':REGENERATION,
                    'CAPACITY_LEVEL':CAPACITY_LEVEL,'player_id':player_id,
                    'people':people,'shit':shit,'capacity':capacity,'nature':nature}
            print cell
create_map(2,5)