from uuid import uuid4
import json
import os

class FileDatabase():
    
    filename = None
    database = {}
    callbacks = {'insert': None, 'update': None, 'replace': None, 'delete': None}
    
    def __init__(self, filename, callbacks = None):
        if callbacks is not None:
            self.callbacks = callbacks 
        self.filename = filename
        self.load()
        
    async def list(self, limit = None, offset = None):
        return list(self.database.values())
    
    # TODO - limit and offset
    async def find(self, search_criteria = None, limit = None, offset = None):
        results = []
        for record in list(self.database.values()):
            ok = True
            if search_criteria is not None:
                for field in search_criteria:
                    value = search_criteria[field]
                    if value is not None:
                        if (record[field] != value):
                            ok = False
                            break
            if ok:
                results.append(record)
            return results
    
        
    async def get(self, id):
        return self.database.get(id)
        
    async def insert(self, data):
        id = str(uuid4())
        data    ['_id'] = id
        self.database[id] = data
        self.save()
        if 'insert' in self.callbacks and self.callbacks['insert']:
            self.callbacks['insert']('insert',self.database[id])
            
    async def update(self, id, data):
        for d in data:
            self.database[id][d] = data[d]
        self.save()
        if 'update' in self.callbacks and self.callbacks['update']:
            self.callbacks['update']('update',self.database[id])
            
    async def replace(self, id, data):
        self.database[id] = data
        self.save()
        if 'replace' in self.callbacks and self.callbacks['replace']:
            self.callbacks['replace']('replace',self.database[id])
    
    async def delete(self, id):
        if 'delete' in self.callbacks and self.callbacks['delete']:
            self.callbacks['delete']('delete',self.database[id])
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
