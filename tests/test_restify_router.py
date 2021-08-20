from fastapi import FastAPI
from fastapi.testclient import TestClient
import motor
import sys
import os
import json
from pydantic import BaseModel, EmailStr, Field
from pymongo_inmemory import Mongod
import asyncio
import uvicorn
import requests
import time
from typing import Optional
from httpx import AsyncClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")

from restful_router import get_router
from mongo_database import MongoDatabase

from web_server import WebServer

class MongoMemoryClient(motor.motor_asyncio.AsyncIOMotorClient):
    def __init__(self, host=None, port=None, **kwargs):
        self._mongod = Mongod()
        self._mongod.start()
        super().__init__(self._mongod.connection_string, **kwargs)

    def close(self):
        self._mongod.stop()
        super().close()
        
class TestInsertModel(BaseModel):
    name: str
    age: Optional[int]
    sex: Optional[str]
    items: Optional[list] = []
class TestUpdateModel(BaseModel):
    id: str = Field(..., alias='_id')
    name: Optional[str]
    age: Optional[int]
    sex: Optional[str]
    items: Optional[list] = []
    
class TestModel(MongoDatabase):
    insertModelClass = TestInsertModel
    updateModelClass = TestUpdateModel
    
    def __init__(self, callbacks):
        # for tests, pass client from pymongo_inmemory
        client = MongoMemoryClient()
        super().__init__('testcollection', callbacks, client)
    
base_url = 'http://localhost:8081/test/'



callback_log = []
def log_callback(type, data):
    callback_log.append({type: data})

async def do_test_restify_router():
    # create model inside asyncio function to ensure motor has access to same event loop
    callbacks = {'insert':log_callback, 'update':log_callback, 'replace':log_callback, 'delete':log_callback}
    test_model = TestModel(callbacks)
    app = FastAPI()
    app.include_router(get_router(test_model), tags=["Test"], prefix="/test")
    
    async def delete_all(ac):
        response = await ac.get(base_url)
        for item in response.json().get('data')[0]:
            await ac.delete(base_url + item.get('_id'))


    async with AsyncClient(app=app) as ac:
        async with WebServer(app):
            # while True:
                # await asyncio.sleep(0.1)
            
            time.sleep(1) # ws startup
            # cleanup
            await delete_all(ac)
            # check get all
            response = await ac.get(base_url)
            
            assert response.status_code == 200
            data = response.json().get('data')[0]
            assert data == []
            # post a record
            postresponse = await ac.post(base_url,json=[{'name': 'fred'}])
            response = await ac.get(base_url)
            print(postresponse.json())
            print(response.json())
            # get a record
            getresponse = await ac.get(base_url+response.json().get('data')[0][0].get('_id'))
            assert(getresponse.json().get('data')[0].get('name') == 'fred')
            assert getresponse.status_code == 200
            # put/update a record
            update_data = [{'_id': response.json().get('data')[0][0].get('_id'), 'name': 'joe', 'age': 90}]
            # print('update data')
            # print(update_data)
            updateresponse = await ac.put(base_url, json=update_data)
            assert updateresponse.status_code == 200
            getresponse = await ac.get(base_url+response.json().get('data')[0][0].get('_id'))
            assert(getresponse.json().get('data')[0].get('name') == 'joe')
            assert(getresponse.json().get('data')[0].get('age') == 90)
            # replace a record
            updateresponse = await ac.patch(base_url, json=[{'_id': response.json().get('data')[0][0].get('_id'), 'name': 'sam'}])
            assert updateresponse.status_code == 200
            getresponse = await ac.get(base_url+response.json().get('data')[0][0].get('_id'))
            assert(getresponse.json().get('data')[0].get('name') == 'sam')
            assert(getresponse.json().get('data')[0].get('age', None) == None)
            
            # find a record
            findresponse = await ac.get(base_url + "?filter="+json.dumps({'name': 'sam'}))
            print(findresponse.json())
            assert(findresponse.json().get('data')[0][0].get('name') == 'sam')
            assert(findresponse.json().get('data')[0][0].get('age', None) == None)
            
            # delete a record
            response = await ac.get(base_url)
            deleteresponse = await ac.delete(base_url + response.json().get('data')[0][0].get('_id'))

            response = await ac.get(base_url)
            response = await ac.get(base_url)
            assert response.status_code == 200
            data = response.json().get('data')[0]
            assert data == []
            # print(callback_log)
            assert(callback_log[0].get('insert').get('name') == 'fred')
            assert(callback_log[1].get('update').get('name') == 'joe')
            assert(callback_log[2].get('replace').get('name') == 'sam')
            assert(callback_log[3].get('delete').get('name') == 'sam')
            
def test_restify_router():
    asyncio.run( do_test_restify_router())   

if __name__ == "__main__":
    test_restify_router()
   

