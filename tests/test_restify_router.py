from fastapi import FastAPI
from fastapi.testclient import TestClient
import motor
import sys
import os
from pydantic import BaseModel, EmailStr, Field
from pymongo_inmemory import Mongod
import asyncio
import uvicorn
import requests
import time

from httpx import AsyncClient


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")

from restful_router import get_router
from mongo_database import MongoDatabase

from web_server import WebServer

class MongoClient(motor.motor_asyncio.AsyncIOMotorClient):
    def __init__(self, host=None, port=None, **kwargs):
        self._mongod = Mongod()
        self._mongod.start()
        super().__init__(self._mongod.connection_string, **kwargs)

    def close(self):
        self._mongod.stop()
        super().close()
        
class TestInsertModel(BaseModel):
    name: str
class TestUpdateModel(BaseModel):
    name: str

class TestModel(MongoDatabase):
    insertModelClass = TestInsertModel
    updateModelClass = TestUpdateModel
    
    def __init__(self):
        client = MongoClient()
        super().__init__('testcollection', client)
    
base_url = 'http://localhost:8081/test/'



async def do_test_restify_router():
    # create model inside asyncio function to ensure motor has access to shared loop
    test_model = TestModel()
    app = FastAPI()
    app.include_router(get_router(test_model), tags=["Test"], prefix="/test")
    
    async def delete_all():
        async with AsyncClient(app=app) as ac:
            response = await ac.get(base_url)
            for item in response.json().get('data')[0]:
                await ac.delete(item.get('_id'))

    async with AsyncClient(app=app) as ac:
        async with WebServer(app):
            time.sleep(1) # ws startup
            # cleanup
            await delete_all()
            # check get all
            response = await ac.get(base_url)
            
            assert response.status_code == 200
            data = response.json().get('data')[0]
            assert data == []
            # post a record
            postresponse = await ac.post(base_url,json={'name': 'fred'})
            response = await ac.get(base_url)
            # get a record
            getresponse = await ac.get(base_url+response.json().get('data')[0][0].get('_id'))
            assert(getresponse.json().get('data')[0].get('name') == 'fred')
            assert getresponse.status_code == 200
            # put/update a record
            updateresponse = await ac.put(base_url+response.json().get('data')[0][0].get('_id'), json={'name': 'joe'})
            assert updateresponse.status_code == 200
            getresponse = await ac.get(base_url+response.json().get('data')[0][0].get('_id'))
            assert(getresponse.json().get('data')[0].get('name') == 'joe')
            
            response = await ac.get(base_url)
            
            # delete a record
            deleteresponse = await ac.delete(base_url + response.json().get('data')[0][0].get('_id'))

            response = await ac.get(base_url)
            response = await ac.get(base_url)
            assert response.status_code == 200
            data = response.json().get('data')[0]
            assert data == []
            
def test_restify_router():
    asyncio.run( do_test_restify_router())   

if __name__ == "__main__":
    test_restify_router()
   

