from pymongo import MongoClient
import random
import os
import threading
import time
from bson.objectid import ObjectId
import math

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
        i = 0
        while True:
            self.longwalk()
            i += 1;
            time.sleep(0.1)
            if i > 0: break;
            
    def refresh(self):
        pass
    
    def longwalk(self):
        cursor = self.db.map.find()
        for document in cursor:
            main_data = {}
            for key in self.main_keys:
                main_data[key] = document[key]
            self.step(main_data)
            
    def step(self,main_data):
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
        #print produce_shit
        #FILTERS
        produce_shit -= 0
        #NATURE AND PEOPLE
        main_data['shit'] = main_data['shit'] + produce_shit
        tmp_nature = 0
        if main_data['shit'] < (main_data['nature'] * 0.05):
            #grow
            tmp_nature = main_data['nature'] + (main_data['NATURE_LEVEL'] - main_data['nature'])/main_data['NATURE_LEVEL']
        elif main_data['shit'] > (main_data['nature'] * 0.05) and main_data['shit'] < (main_data['nature'] * 0.26):
            tmp_nature = main_data['nature']
        elif main_data['shit'] > (main_data['nature'] * 0.25) and main_data['shit'] < (main_data['nature']):
            #wither
            tmp_nature = main_data['nature'] - (math.sqrt(main_data['shit']) + main_data['people']**(1/3.0))
            if tmp_nature < 0 : tmp_nature = 0
        elif main_data['shit'] > (main_data['nature']):
            tmp_nature = 0
        main_data['nature'] = tmp_nature
        
        children_of_nature = float(main_data['people']/((main_data['nature']+0.000001)*10))
        print children_of_nature
        if children_of_nature < 0.5:
            print "free"
            main_data['people'] += (main_data['people']/2)
        elif children_of_nature > 0.49 and children_of_nature < 1:
            print "norm"
            main_data['people'] += math.sqrt(main_data['people'])
        elif children_of_nature > 1:
            print "die"
            main_data['people']
            main_data['people'] -= (main_data['people'] - main_data['nature']*10)
            main_data['people']
        elif children_of_nature == 0:
            print "wind"
            
        #REGENERATION MINE
        main_data['capacity'] += main_data['REGENERATION']
        if main_data['capacity'] > main_data['CAPACITY_LEVEL']:
            main_data['capacity'] = main_data['CAPACITY_LEVEL']
       
        self.main_answer(main_data)
        self.spread_shit(main_data)
            
    def main_answer(self,dict_data):      
        self.db.map.update({"_id": ObjectId(dict_data['_id'])},{'$set':self.packing(dict_data,['people','capacity','nature'])})
        
    def spread_shit(self,dict_data):
        self.db.map.update({"_id": ObjectId(dict_data['_id'])},{'$set':self.packing(dict_data,['shit'])})

        
    def packing(self,dict_data,variables):
        tmp_dict = {}       
        for key in variables:
            tmp_dict[key] = dict_data[key]
        return tmp_dict
        
        
        

cellwalker = CellWalker()

