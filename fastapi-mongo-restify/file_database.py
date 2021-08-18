from uuid import uuid4
import json
import os

class FileDatabase():
    
    filename = None
    database = {}
    
    def __init__(self, filename):
        self.filename = filename
        self.load()
        
    async def list(self):
        return list(self.database.values())
    
    # TODO
    async def find(self):
        for record in list(self.database.values()):
            print(record)
    
        
    async def get(self, id):
        return self.database.get(id)
        
    async def insert(self, data):
        id = str(uuid4())
        data    ['_id'] = id
        self.database[id] = data
        self.save()
    
    async def update(self, id, data):
        for d in data:
            self.database[id][d] = data[d]
        self.save()
    
    async def delete(self, id):
        self.database.pop(id)
        self.save()
        return True
        

    # internal functions
    def save(self):
        if not os.path.isdir(os.path.dirname(self.filename)):
            os.mkdir(os.path.dirname(self.filename))
        f = open(self.filename, "w")
        j = json.dumps( self.database)
        f.write(j)
        f.close()
        
    def load(self):
        # print('load')
        try:
            f = open(self.filename, "r")
            j = json.loads(f.read())
            self.database = j
            
        except json.JSONDecodeError:
            self.database = {}
        except FileNotFoundError:    
            self.database = {}
