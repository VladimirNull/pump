from pymongo import MongoClient
import random
import os
import time

client = MongoClient()
db = client.test


def create_map(len_x,len_y):
    os.system('clear')
    for i in range(len_y):
        for g in range(len_y):
            x,y = g,i
            NATURE_LEVEL = random.randrange(1,10)
            PRESSURE = random.randrange(1,10)
            MANA_GOLD = round(float(random.randrange(51,95))/100,2)
            MANA_SHIT = round((1 - MANA_GOLD),2)
            REGENERATION = random.randrange(1,10)
            CAPACITY_LEVEL = random.randrange(10,1000)
            player_id = None
            people = 100
            shit = 0
            capacity = CAPACITY_LEVEL
            nature = NATURE_LEVEL
            
            cell = {'x':x,'y':y,'NATURE_LEVEL':NATURE_LEVEL,'PRESSURE':PRESSURE,
                    'MANA_GOLD':MANA_GOLD,'MANA_SHIT':MANA_SHIT,'REGENERATION':REGENERATION,
                    'CAPACITY_LEVEL':CAPACITY_LEVEL,'player_id':player_id,
                    'people':people,'shit':shit,'capacity':capacity,'nature':nature}

            print cell
            db.map.insert(cell)
def read_map():
    cursor = db.map.find()
    for document in cursor:
        print document
        if str(document['_id']) == '594c221f77097b2878b9c859':
            print document
def delete_map():
    cursor = db.map.drop()
    
read_map()  
i = 0
while False:
    read_map()
    i += 1;
    time.sleep(0.5)
    os.system('clear')
    if i > 100: break;