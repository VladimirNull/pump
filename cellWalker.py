from pymongo import MongoClient
import random
import os
import threading
import time

class CellWalker(object):
    def __init__(self):
        self.timer = time.time()
        self.db = MongoClient().test
        self.main_keys = ('NATURE_LEVEL', 'PRESSURE', 'MANA_GOLD', 
                     'MANA_SHIT', 'REGENERATION', 'CAPACITY_LEVEL',
                     'player_id', 'people', 'shit', 'capacity','nature','_id')
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True 
        thread.start()
        
    def __str__(self):
        return "there is nothing to see"
        
    def run(self):
        while True:
            self.longwalk()
            break;
            
    def refresh(self):
        pass
    
    def longwalk(self):
        cursor = self.db.map.find()
        for document in cursor:
            main_data = {}
            for key in self.main_keys:
                main_data[key] = document[key]
            self.step(main_data,document['_id'])
            
    def step(self,main_data,id_cell):
        produce_shit = 0
        #print main_data
        #MINE
        if main_data['capacity'] == 0:
            packets_pumped = 0
        else:  
            packets_pumped = main_data['PRESSURE']
            if main_data['capacity'] - packets_pumped < 0:
                packets_pumped = main_data['capacity']
                main_data['capacity'] = 0
            else:
                main_data['capacity'] -= packets_pumped
        #FACTORY
        gold = packets_pumped * main_data['MANA_GOLD']
        produce_shit += packets_pumped * main_data['MANA_SHIT']
        #FILTERS
        produce_shit -= 0
        #NATURE
        main_data['nature'] -= produce_shit
        if main_data['nature']>=0:
            main_data['people'] += main_data['nature']
        else:
            main_data['people'] -= main_data['nature']
        #REGENERATION MINE
        main_data['capacity'] += main_data['REGENERATION']
        if main_data['capacity'] > main_data['CAPACITY_LEVEL']:
            main_data['capacity'] = main_data['CAPACITY_LEVEL']
        if str(id_cell)=='594abcdc77097b12bed7543a':
            print main_data['people'],main_data['capacity'],main_data['nature']
        
        
        

cellwalker = CellWalker()

