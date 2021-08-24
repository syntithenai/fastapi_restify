from uuid import uuid4
import json
import os

import motor.motor_asyncio
from bson import ObjectId
from mongo_connect import mongo_connect
from decouple import config

class MongoDatabase():
    
    client = None
    collectionName = None
    model = None
    callbacks = {}
    
    def __init__(self, collection_name, callbacks = None, client_param = None):
        # print(f"INIT {collection_name}")
        self.collection_name = collection_name
        if callbacks is not None:
            self.callbacks = callbacks
        # allow injecting client for tests
        if client_param is not None:
            self.client = client_param
        # else:
            # # mongo_uri = config('MONGO_URI','')
            # # client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
            # self.client = db_client
    
    async def get_collection(self):    
        if self.client is None:
            self.client = await mongo_connect.get_db_client()
        if self.client is not None:
            # print(type(self.client))
            # print(self.client)
            database = self.client[config('MONGO_DATABASE')]
            collection = database.get_collection(self.collection_name)
            return collection
        else:
            return None
        
    async def list(self, limit = None, offset = None):
        collection = await self.get_collection()
        if collection is not None:
            items = []
            cursor = collection.find()
            if offset is not None:
                cursor.skip(offset)
            if limit is not None:
                cursor.limit(limit)
            async for item in cursor:
                item['_id'] = str(item.get('_id'))
                items.append(self.to_dict(item))
            return items
        
    async def find(self, criteria, limit = None, offset = None):
        collection = await self.get_collection()
        if collection is not None:
            items = []
            cursor = collection.find(criteria)
            if offset is not None:
                cursor.skip(offset)
            if limit is not None:
                cursor.limit(limit)
            async for item in cursor:
                item['_id'] = str(item.get('_id'))
                items.append(self.to_dict(item))
            return items
        
    async def get(self, id):
        collection = await self.get_collection()
        if collection is not None:
            item = await collection.find_one({"_id": ObjectId(id)})
            if item:
                item['_id'] = str(item.get('_id'))
                return self.to_dict(item)
      
    async def insert(self, data):
        collection = await self.get_collection()
        if collection is not None:
            result = await collection.insert_one(data)
            new_data = await collection.find_one({"_id": result.inserted_id})
            new_data['_id'] = str(new_data.get('_id'))
            d = self.to_dict(new_data)
            if 'insert' in self.callbacks and self.callbacks['insert']:
                self.callbacks['insert']('insert',new_data)
            return self.to_dict(new_data)
    
    async def update(self, id, data):
        collection = await self.get_collection()
        if collection is not None:
            item = await collection.find_one({"_id": ObjectId(id)})
            if item:
                try:
                    data.pop('_id')
                except KeyError:
                    pass
                await collection.update_one({"_id": ObjectId(id)}, {"$set": data})
                if 'update' in self.callbacks and self.callbacks['update']:
                    item = await collection.find_one({"_id": ObjectId(id)})
                    item['_id'] = str(item.get('_id'))
                    self.callbacks['update']('update',item)            
                return True
            return False
        
    async def replace(self, id, data):
        collection = await self.get_collection()
        if collection is not None:
            item = await collection.find_one({"_id": ObjectId(id)})
            if item:
                try:
                    data.pop('_id')
                except KeyError:
                    pass
                await collection.replace_one({"_id": ObjectId(id)}, data)
                if 'replace' in self.callbacks and self.callbacks['replace']:
                    item = await collection.find_one({"_id": ObjectId(id)})
                    item['_id'] = str(item.get('_id'))
                    self.callbacks['replace']('replace',item)            
                return True
            return False
        
    
    async def delete(self, id):
        collection = await self.get_collection()
        if collection is not None:
            item = await collection.find_one({"_id": ObjectId(id)})
            if item:
                if 'delete' in self.callbacks and self.callbacks['delete']:
                    item['_id'] = str(item.get('_id'))
                    self.callbacks['delete']('delete',item)
                await collection.delete_one({"_id": ObjectId(id)})
                return True
            return False
      
    # override in child class to customise return values from list/get
    def to_dict(self, data): 
        return data
     
