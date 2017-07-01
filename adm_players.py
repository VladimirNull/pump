import random
from bson.objectid import ObjectId
from pymongo import MongoClient
import sys
import time
import os

client = MongoClient()
db = client.test

def create_players(n):
    for i in range(n):
        NAME = "num",random.randrange(0,9),random.randrange(0,9),random.randrange(0,9)
        gold = 0
        cells = []
        player = {'NAME':NAME,'cells':cells,'gold':gold}
        db.players.insert(player)
        
def delete_players():
    cursor = db.players.drop()

def random_cell():
    client = MongoClient()
    db = client.test
    cursor = db.map.find()
    return cursor[random.randrange(0,cursor.count())]['_id']

def random_player():
    client = MongoClient()
    db = client.test
    cursor = db.players.find()
    return cursor[random.randrange(0,cursor.count())]['_id']

def read_players():
    cursor = db.players.find()
    for document in cursor:
        print document

def append_cell():
    rnd_pl = random_player()
    rnd_ce = random_cell()
    db.players.update({"_id": ObjectId(rnd_pl)},{'$push':{'cells':rnd_ce}})
    db.map.update({"_id": ObjectId(rnd_ce)},{'$set':{'player_id':rnd_pl}})

try:
    answ = sys.argv[1]
except:
    answ = None

if answ=='1':
    while True:
        read_players()
        time.sleep(0.1)
        os.system('clear')

elif answ == '2':      
    delete_players()
    
elif answ == '3':
    create_players(1)

elif answ == '4':
    read_players()

    
    