from mongo_database import MongoDatabase

from pydantic import BaseModel, EmailStr, Field

# used to map request parameters on insert/post
class InsertOrderModel(BaseModel):
    name : str
    status: str
    time_started: int
    time_completed: int
    items: tuple

    class Config:
        schema_extra = {
            "example": {
                "name": "order_1",
                "stats": "new",
                "time_started": 0,
                "time_completed": 0,
                "items": tuple()
            }
        }
        
# used to map request parameters on update/put
class UpdateOrderModel(BaseModel):
    name : str
    status: str
    time_started: int
    time_completed: int
    items: tuple

    class Config:
        schema_extra = {
            "example": {
                "name": "order_1_up",
                "stats": "pending",
                "time_started": 2,
                "time_completed": 0,
                "items": tuple()
            }
        }
    
    
class OrdersModel(MongoDatabase):
    # used by router for parameter mapping
    updateModelClass = UpdateOrderModel
    insertModelClass = InsertOrderModel
    
    def __init__(self, name = 'orders'): #name = './file_database/animals.json'):
        super().__init__(name)
    

# singleton    
orders_model = OrdersModel()
