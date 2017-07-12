from pymongo import MongoClient
import random
import os
import threading
import time
from bson.objectid import ObjectId
import math
import threading
from Queue import Queue

class CellWalker(object):
    def __init__(self):
        self.num_threads = 4
        self.timer = time.time()
        self.db = MongoClient().test
        self.main_keys = ('NATURE_LEVEL', 'PRESSURE', 'MANA_GOLD', 
                     'MANA_SHIT', 'REGENERATION', 'CAPACITY_LEVEL',
                     'player_id', 'people', 'shit', 'capacity','nature','_id','pump_level')        
        self.slice_row = self.slice_map(self.num_threads)
        self.row_all_cells = self.all_cells()
        #self.q = Queue()
        #self.run_tasks()
        
    def __str__(self):
        return "there is nothing to see"
    
    def all_cells(self):
        tmp = []
        cursor = self.db.map.find()
        for doc in cursor:
            tmp.append(doc['_id'])
        return tmp
        
    def run_tasks(self):
        for task in self.slice_row:
            self.q.put(task)
        for i in range(4):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True 
            thread.start()
    
    def worker(self):
        while True:
            task = self.q.get()
            self.walkrow(task) 
            self.q.task_done()
    
    def slice_map(self,bt):
        tmp = []
        cursor = self.db.map.find()
        length_cursor = cursor.count()-1
        if length_cursor == -1:
            return False
        cnt = length_cursor // bt
        pntr = 0
        for i in range(1,bt):
            a_pntr = pntr
            pntr+=cnt
            b_pntr = pntr
            pntr+=1
            tmp.append([a_pntr,b_pntr])
        b_pntr += 1
        if b_pntr!=length_cursor:
            tmp.append([b_pntr,length_cursor])
        pntr = 0
        ver_tmp = []
        for verify in tmp:
            if verify[0]<verify[1] and verify[1] > pntr:
                ver_tmp.append(verify)
                pntr = verify[1]+1
        if ver_tmp == []:
            return [cursor[0]['_id']]
        ret_row = []
        print "building ids of map"
        for i in ver_tmp:
            tmp_row = []
            for g in range(i[0],i[1]):
                tmp_row.append(cursor[g]['_id'])
            ret_row.append([tmp_row])
        return ret_row            
    
    def walkrow(self,row = []):#one lap over map
        row.append(self.row_all_cells)
        cursor = self.db.map.find({"_id": { "$in": row[0] } })
        for document in cursor:
            main_data = {}
            for key in self.main_keys:
                main_data[key] = document[key]
            if main_data['player_id'] == None:
                self.relax(main_data)
            else:
                self.step(main_data)
            
    def mine(self,capacity,packets_pumped):
        #TODO random
        if capacity - packets_pumped < 0:
            ret_packets_pumped = capacity
            ret_capacity = 0
        else:
            ret_packets_pumped = packets_pumped
            ret_capacity = capacity - packets_pumped
        return ret_capacity,ret_packets_pumped

    def factory(self,packets_pumped,mana_gold,mana_shit):
        #TODO random
        return packets_pumped * mana_gold, packets_pumped * mana_shit
        
    def filters(self,shit,produce_shit):
        #TODO clean shit
        return shit+produce_shit
        
    def nature_in(self,nature,shit,nature_level,people):
        junk_yard = ((nature)*20)/(shit+0.0001)# 1 tree vs 20 piece of shit
        
        if junk_yard > 1:#grow
            tmp_nature = nature + ((nature_level - nature)/100)
            if tmp_nature > nature: 
                tmp_nature = nature_level
                
        elif junk_yard > 0.80 and junk_yard < 1:#constantly
            tmp_nature = nature
            
        elif junk_yard > 0.20 and junk_yard < 0.80:#wither
            bad_people = (abs(people)**(1/3.0))/500
            bad_shit = (math.sqrt(shit))/300
            tmp_nature = nature - (bad_people + bad_shit)            
                
        elif junk_yard > 0 and junk_yard < 0.20:#great wither
            bad_people = (abs(people)**(1/3.0))/350
            bad_shit = (math.sqrt(shit))/195
            tmp_nature = nature - (bad_people + bad_shit)
                
        elif junk_yard == 0:#wind
            tmp_nature = 0
            
        if tmp_nature < 0 : tmp_nature = 0    
        return tmp_nature
    
    def people_in(self,people,nature,shit):
        #TODO activate shit
        tmp_people = 0
        perform_people = (nature)*10 # 1 tree vs 100 people
        children_of_nature = ((nature)*10)/(people+0.0001)
        if children_of_nature > 1:#free
            born = (people/4)+random.randrange(1, int(abs(people)**(1/3.0)+2)  )
            tmp_people = people + born
        elif children_of_nature > 0.49 and children_of_nature < 1:#norm
            tmp_people = people + (math.sqrt(people)/4)
        elif children_of_nature < 0.5:#help us
            #TODO this
            tmp_people = people - (math.sqrt(people)+random.randrange(1, (int(abs(people)**(1/3.0))+2)   ))
        if tmp_people < 0 or (round(tmp_people) == 0.0):
            tmp_people = 0
        return tmp_people
        
    def regeneration_mine(self,regeneration,capacity,capacity_level):
        capacity += (float(regeneration)/100)+(float(random.randrange(1,10))/200)
        if capacity > capacity_level: 
            capacity = capacity_level
        return capacity
        
    def regeneration_nature(self,nature_level,nature):
        if (nature_level > nature):
            nature += math.sqrt(nature_level - nature)  
        else:
            nature -= math.sqrt(nature - nature_level)
        return nature
    
    def clean_shit(self,nature,shit):
        shit = shit - nature
        shit = 0 if shit <= 0 else shit
        return shit

    def step(self,main_data):
        #MINE
        main_data['capacity'],packets_pumped = (self.mine(main_data['capacity'],(main_data['PRESSURE']*main_data['pump_level'])))
        
        #FACTORY
        gold,produce_shit = (self.factory(packets_pumped,main_data['MANA_GOLD'],main_data['MANA_SHIT']))
        
        #FILTERS
        main_data['shit'] = self.filters(main_data['shit'],produce_shit)
        
        #NATURE
        main_data['nature'] = self.nature_in(main_data['nature'],main_data['shit'],main_data['NATURE_LEVEL'],main_data['people'])
        
        #PEOPLE
        main_data['people'] = self.people_in(main_data['people'],main_data['nature'],main_data['shit'])
        
        #REGENERATION MINE
        main_data['capacity'] = self.regeneration_mine(main_data['REGENERATION'], main_data['capacity'],main_data['CAPACITY_LEVEL'])
        
        #send results
        self.main_answer(main_data)
        self.spread_shit(main_data)
        self.profit_play(main_data,gold)
            
    def main_answer(self,dict_data):      
        self.db.map.update({"_id": ObjectId(dict_data['_id'])},{'$set':self.packing(dict_data,['people','capacity','nature'])})
        
    def spread_shit(self,dict_data):
        self.db.map.update({"_id": ObjectId(dict_data['_id'])},{'$set':self.packing(dict_data,['shit'])})
    
    def profit_play(self,dict_data,gold):
        self.db.players.update({"_id": ObjectId(dict_data['player_id'])},{'$inc':{'gold':gold}})
        
    def packing(self,dict_data,variables):
        tmp_dict = {}       
        for key in variables:
            tmp_dict[key] = dict_data[key]
        return tmp_dict    
        
    def relax(self,main_data):
        if main_data['NATURE_LEVEL'] == main_data['nature'] and main_data['CAPACITY_LEVEL'] == main_data['capacity'] and main_data['shit'] == 0:
            pass
        else:
            if main_data['NATURE_LEVEL'] == round(main_data['nature']) and main_data['CAPACITY_LEVEL'] == round(main_data['capacity']) and round(main_data['shit']) == 0:
                main_data['nature'] = main_data['NATURE_LEVEL']
                main_data['capacity'] = main_data['CAPACITY_LEVEL']
                main_data['shit'] = 0
            else:
                main_data['capacity'] = self.regeneration_mine(main_data['REGENERATION'], main_data['capacity'],main_data['CAPACITY_LEVEL'])
                main_data['nature'] = self.regeneration_nature(main_data['NATURE_LEVEL'],main_data['nature'])
                main_data['shit'] = self.clean_shit(main_data['nature'], main_data['shit'])
            self.db.map.update({"_id": ObjectId(main_data['_id'])},{'$set':self.packing(main_data,['nature','capacity','shit'])})
            