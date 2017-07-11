from pymongo import MongoClient
import random
import os
import time
from bson.objectid import ObjectId

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
            print doc['_id'],doc['player_id'],"x=",doc['x'],"y=",doc['y']
    
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
    
    def showtv(self,player_id,xr,yr):
        player = self.players.find({"_id": ObjectId(player_id)})
        x_player = player[0]['cursor_view'][0]
        y_player = player[0]['cursor_view'][1]
        print "x,y",x_player,y_player
        cells = db.map.find({'$and':[{'x':{'$gte':x_player-xr}},{'x':{'$lte':x_player+yr}},\
                                     {'y':{'$gte':x_player-xr}},{'y':{'$lte':x_player+yr}}]})
        for cell in cells:
            print cell['x'],cell['y']
        
    

client = MongoClient()
db = client.test            
ps = PlayersSpace()
ps.show_db()

ps.showtv('59650c9677097b14458e0593',1,1)