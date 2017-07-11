import random
from bson.objectid import ObjectId
from pymongo import MongoClient
import sys
import time
import os

sys.path.append(os.path.dirname(os.path.realpath(sys.argv[0])))
from cellWalker import *
from playersSpace import *

client = MongoClient()
db = client.test

def create_players(n):
    for i in range(n):
        NAME = "num",random.randrange(0,9),random.randrange(0,9),random.randrange(0,9)
        gold = 0
        cells = []
        cursor_view = [5,5]
        player = {'NAME':NAME, 'cells':cells, 'gold':gold, 'cursor_view':cursor_view}
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
    
def create_pl():  
    create_players(1)

player_select = None

client = MongoClient()
db = client.test            
ps = PlayersSpace()
ps.show_db()

while True:
    print "1.step\n2.player manage\n3.administration\nq.Quit"
    answ1 = raw_input("input.")
    if answ1 == "1":
        print "coming soon"
    elif answ1 == "2":
        while True:
            print "player_select ",player_select
            print "1.select player\n2.add cell\nq.Quit"
            answ3 = raw_input("input.")
            if answ3 == "1":
                cursor = db.players.find()
                i = 0
                for document in cursor:
                    print i,document['_id']
                    i += 1
                answ4 = raw_input("input number id")
                cursor = db.players.find()
                player_select = cursor[int(answ4)]['_id']       
    elif answ1 == 3:        
        print "1.create player\n2.delete players\n3.show players\nq.Quit"
        answ2 = raw_input("Ask user for something.")
        if answ2 == "1":
            create_players(1)
        elif answ2 == "2":
            delete_players()
        elif answ2 == "3":
            read_players()
        elif answ2 == "q":
            break
        
    
    