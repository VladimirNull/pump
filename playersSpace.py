from pymongo import MongoClient
import random
import os
import time
from bson.objectid import ObjectId

client = MongoClient()
db = client.test

class PlayersSpace(object):
    def __init__(self):
        self.players = db.players
    def __str__(self):
        return "nothing to see here"
        
    def create_player(self):
        gold = 100
        cells_master = [] # ids cells        
        cell = {'gold':gold,'cells_master':cells_master}
        self.players.insert(cell)
        
    def show_players(self):
        tmp = []
        cursor = self.players.find()
        for document in cursor:
            tmp.append(document)
        return tmp
        
    def delete_player(self,player_id):
        result = self.players.delete_one({'_id': ObjectId(player_id)})
    
    def cell_for_grab(self,cell_id):
        cell = db.map.find({'_id': ObjectId(cell_id)})
        if cell.count() == 1:#cell excists          
            if cell[0]['player_id'] == None:#cell grabable
                return True
        return False
    
    def cell_for_free(self,cell_id,player_id):
        cell = self.players.find({'_id': ObjectId(player_id)})
    
    def show_db(self):
        player = self.players.find()
        for doc in player:
            print doc['_id']
            print "master",doc['cells']
        print "========="
        cell = db.map.find()
        for doc in cell:
            print doc['_id'],doc['player_id']
    
    def grab_cell(self,cell_id,player_id):
        player = self.players.find({'_id': ObjectId(player_id)})
        if player.count() == 1:#player isset
            if self.cell_for_grab(cell_id):
                self.players.update({"_id": ObjectId(player_id)},{'$push':{'cells':cell_id}})
                db.map.update({"_id": ObjectId(cell_id)},{'$set':{'player_id':player_id}})        
    
    def free_cell(self,cell_id,player_id):
        player = self.players.find({"_id": ObjectId(player_id)})
        cell = db.map.find({'_id': ObjectId(cell_id)})
        if player.count() == 1 and cell.count() == 1:
            if cell_id in player[0]['cells']:
                mass = player[0]['cells']
                mass.remove(cell_id)
                self.players.update({"_id": ObjectId(player_id)},{'$set':{'cells':mass}})
                db.map.update({"_id": ObjectId(cell_id)},{'$set':{'player_id':None}})
            
        

ps = PlayersSpace()
ps.show_db()