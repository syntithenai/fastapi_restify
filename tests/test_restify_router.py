from fastapi import FastAPI
from fastapi.testclient import TestClient
import motor
import sys
import os
from pydantic import BaseModel, EmailStr, Field
from pymongo_inmemory import Mongod

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")

from restful_router import get_router
from mongo_database import MongoDatabase

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
    
test_model = TestModel()

app = FastAPI()
app.include_router(get_router(test_model), tags=["Test"], prefix="")
client = TestClient(app)

def delete_all():
    response = client.get("/")
    for item in response.json().get('data')[0]:
        client.delete(item.get('_id'))


def test_restify_router():
    delete_all()
    # check get all
    response = client.get("/")
    assert response.status_code == 200
    data = response.json().get('data')[0]
    assert data == []
    # post a record
    response = client.post("/",json={'name': 'fred'})
    # get a record
    getresponse = client.get("/"+response.json().get('data')[0].get('_id'))
    assert(getresponse.json().get('data')[0].get('name') == 'fred')
    assert getresponse.status_code == 200
    # put/update a record
    updateresponse = client.put("/"+response.json().get('data')[0].get('_id'), json={'name': 'joe'})
    assert updateresponse.status_code == 200
    getresponse = client.get("/"+response.json().get('data')[0].get('_id'))
    assert(getresponse.json().get('data')[0].get('name') == 'joe')
    # delete a record
    deleteresponse = client.delete(response.json().get('data')[0].get('_id'))
    response = client.get("/")
    assert response.status_code == 200
    data = response.json().get('data')[0]
    assert data == []
    
    

if __name__ == "__main__":
    test_restify_router()
