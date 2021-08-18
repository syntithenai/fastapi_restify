from file_database import FileDatabase

from pydantic import BaseModel, EmailStr, Field

# used to map request parameters on insert/post
class InsertProductModel(BaseModel):
    name : str
    price: str
    image: str
    class Config:
        schema_extra = {
            "example": {
                "name": "burger",
                "price": "5.00",
                "image": ""
            }
        }
        
# used to map request parameters on update/put
class UpdateProductModel(BaseModel):
    name : str
    price: str
    image: str
    class Config:
        schema_extra = {
            "example": {
                "name": "burger",
                "price": "6.00",
                "image": ""
            }
        }
        

class ProductsModel(FileDatabase):
    # used by router for parameter mapping
    updateModelClass = UpdateProductModel
    insertModelClass = InsertProductModel
    
    
    def __init__(self, name = './file_database/products.json'):
        super().__init__(name)
    
# singleton    
products_model = ProductsModel()
    
