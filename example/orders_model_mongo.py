from mongo_database import MongoDatabase
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from products_model_file import InsertProductModel, UpdateProductModel

# used to map request parameters on insert/post
class InsertOrderModel(BaseModel):
    name : str
    status: str
    time_started: int
    time_completed: int
    items: List[InsertProductModel] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "order_1",
                "status": "new",
                "time_started": 0,
                "time_completed": 0,
                "items": []
            }
        }
        
# used to map request parameters on update/put
class UpdateOrderModel(BaseModel):
    id: str = Field(..., alias='_id')
    name : str
    status: str
    time_started: int
    time_completed: int
    items: List[UpdateProductModel] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "order_1_up",
                "status": "pending",
                "time_started": 2,
                "time_completed": 0,
                "items": [{'_id':'a2342ser24', 'name': 'pizza'}]
            }
        }
    
    
class OrdersModel(MongoDatabase):
    # used by router for parameter mapping
    updateModelClass = UpdateOrderModel
    insertModelClass = InsertOrderModel
    
    
    def __init__(self, name = 'orders', callbacks = None): #name = './file_database/animals.json'):
        super().__init__(name, callbacks)
    

# singleton    
orders_model = OrdersModel()
