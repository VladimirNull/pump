from pymongo import MongoClient
import random
import os
import time

client = MongoClient()
db = client.test

class PlayesSpace(object):
    def __init__(self):
def create_player():
    gold = 100
    cells_master = [] # ids cells
    
    cell = {'gold':gold,'cells_master':cells_master}
    
    print cell
    db.players.insert(cell)
def show_players():
    cursor = db.players.find()
    for document in cursor:
        print document

