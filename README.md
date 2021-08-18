# FastAPI Restify

This project helps create a restful api using FastAPI and pydantic with storage engines including file and mongodb.

The project uses pydantic to map incoming request body data into a storage format.

The project provides
- File database implementing list, get, insert, update, delete
- Mongo database implementing list, get, insert, update, delete
- FastAPI router with routes for each HTTP verb get, post, put, delete

This project is based on the example provided by https://github.com/Youngestdev/fastapi-mongo.


## Usage

1. First up install the package
```pip install fastapi_mongo_restify```


2. Then create a model object that extends MongoDatabase (or FileDatabase)
- provides pydantic model classes as class variables, updateModelClass and insertModelClass.
The insert model is applied to parsing POST requests and the update model is used for PUT requests.
- calls super().__init('collectionName') in it's constructor


```
from fastapi_mongo_restify.mongo_database import MongoDatabase

from pydantic import BaseModel, EmailStr, Field

# used to map request parameters on insert/post
class InsertOrderModel(BaseModel):
    name : str
    status: str
    time_started: int
    time_completed: int
        
# used to map request parameters on update/put
class UpdateOrderModel(BaseModel):
    name : str
    status: str
    time_started: int
    time_completed: int
   
class OrdersModel(MongoDatabase):
    # used by router for parameter mapping
    updateModelClass = UpdateOrderModel
    insertModelClass = InsertOrderModel
    
    def __init__(self, name = 'orders'): 
        super().__init__(name)
```

3. Use the restify router in your app, passing an instance of your model to the router and specifying the url prefix.

```
from fastapi import FastAPI, Depends
from fastapi_mongo_restify.restful_router import get_router
from orders_model_mongo import OrdersModel
orders_model = OrdersModel()

app = FastAPI(title='Test FastAPI Mongo Restify')
app.include_router(get_router(orders_model), tags=["Orders"], prefix="/orders") 

```
4. start your app with uvicorn
```
import uvicorn

if __name__ == '__main__':
    uvicorn.run('app:app', host="0.0.0.0", port=8080, reload=True)
```

5. Open [http://localhost:8080/docs](http://localhost:8080/docs) to see the FASTAPI generated documentation for your API.