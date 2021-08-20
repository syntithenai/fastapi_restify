from uuid import uuid4
import json
import os

import motor.motor_asyncio
from bson import ObjectId
from decouple import config

class MongoDatabase():
    
    collection = None
    model = None
    callbacks = {}
    
    def __init__(self, collectionName, callbacks = None, clientParam = None):
        if callbacks is not None:
            self.callbacks = callbacks
        # allow injecting client for tests
        if clientParam is not None:
            client = clientParam
        else:
            mongo_uri = config('MONGO_URI','')
            client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        database = client[config('MONGO_DATABASE','')]
        self.collection = database.get_collection(collectionName)
        
    async def list(self):
        items = []
        async for item in self.collection.find():
            item['_id'] = str(item.get('_id'))
            items.append(self.to_dict(item))
        return items
        
    async def find(self, criteria):
        items = []
        async for item in self.collection.find(criteria):
            item['_id'] = str(item.get('_id'))
            items.append(self.to_dict(item))
        return items
        
    async def get(self, id):
        item = await self.collection.find_one({"_id": ObjectId(id)})
        if item:
            item['_id'] = str(item.get('_id'))
            return self.to_dict(item)
      
    async def insert(self, data):
        result = await self.collection.insert_one(data)
        new_data = await self.collection.find_one({"_id": result.inserted_id})
        new_data['_id'] = str(new_data.get('_id'))
        d = self.to_dict(new_data)
        if 'insert' in self.callbacks and self.callbacks['insert']:
            self.callbacks['insert']('insert',new_data)
        return self.to_dict(new_data)
    
    async def update(self, id, data):
        item = await self.collection.find_one({"_id": ObjectId(id)})
        if item:
            data.pop('_id')
            await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            if 'update' in self.callbacks and self.callbacks['update']:
                item = await self.collection.find_one({"_id": ObjectId(id)})
                item['_id'] = str(item.get('_id'))
                self.callbacks['update']('update',item)            
            return True
        return False
        
    async def replace(self, id, data):
        item = await self.collection.find_one({"_id": ObjectId(id)})
        if item:
            data.pop('_id')
            await self.collection.replace_one({"_id": ObjectId(id)}, data)
            if 'replace' in self.callbacks and self.callbacks['replace']:
                item = await self.collection.find_one({"_id": ObjectId(id)})
                item['_id'] = str(item.get('_id'))
                self.callbacks['replace']('replace',item)            
            return True
        return False
        
    
    async def delete(self, id):
        item = await self.collection.find_one({"_id": ObjectId(id)})
        if item:
            if 'delete' in self.callbacks and self.callbacks['delete']:
                item['_id'] = str(item.get('_id'))
                self.callbacks['delete']('delete',item)
            await self.collection.delete_one({"_id": ObjectId(id)})
            return True
        return False
      
    # override in child class to customise return values from list/get
    def to_dict(self, data): 
        return data
     
