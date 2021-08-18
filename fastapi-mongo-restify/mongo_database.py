from uuid import uuid4
import json
import os

import motor.motor_asyncio
from bson import ObjectId
from decouple import config

class MongoDatabase():
    
    collection = None
    model = None
    
    def __init__(self, collectionName):
        mongo_uri = config('MONGO_URI')
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        database = client[config('MONGO_DATABASE')]
        self.collection = database.get_collection(collectionName)
        
    async def list(self):
        items = []
        async for item in self.collection.find():
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
        new_data = await self.collection.find_one({"_id": result.inserted_id},{'_id': 0})
        new_data['_id'] = str(new_data.get('_id'))
        d = self.to_dict(new_data)
        return self.to_dict(new_data)
        
    
    async def update(self, id, data):
        item = await self.collection.find_one({"_id": ObjectId(id)})
        if item:
            await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            return True
        return False
    
    async def delete(self, id):
        item = await self.collection.find_one({"_id": ObjectId(id)})
        if item:
            await self.collection.delete_one({"_id": ObjectId(id)})
            return True
        return False
      
    # override in child class to customise return values from list/get
    def to_dict(self, data): 
        return data
     
