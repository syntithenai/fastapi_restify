from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
import sys
import os
from decouple import config
import motor.motor_asyncio
from bson import ObjectId
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )

from auth.admin_model import AdminModel

from auth.jwt_handler import signJWT

mongo_uri = config('MONGO_URI')
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
database = client[config('MONGO_DATABASE')]
admin_collection = database.get_collection('admin_users')

async def add_admin(admin_data: dict) -> dict:
    admin = await admin_collection.insert_one(admin_data)
    new_admin = await admin_collection.find_one({"_id": admin.inserted_id})
    return admin_helper(new_admin)
    

def admin_helper(admin) -> dict:
    return {
        "id": str(admin['_id']),
        "fullname": admin['fullname'],
        "email": admin['email'],
    }

    
router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@router.post("/login")
async def admin_login(admin_credentials: HTTPBasicCredentials = Body(...)):
    # NEW CODE
    admin_user = await admin_collection.find_one({"email": admin_credentials.username}, {"_id": 0})
    if (admin_user):
        password = hash_helper.verify(
            admin_credentials.password, admin_user["password"])
        if (password):
            return signJWT(admin_credentials.username)
        return "Incorrect email or password"
    return "Incorrect email or password"

@router.post("/create_user")
async def admin_signup(admin: AdminModel = Body(...)):
    admin_exists = await admin_collection.find_one({"email":  admin.email}, {"_id": 0})
    if(admin_exists):
        return "Email already exists"
    
    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(jsonable_encoder(admin))
    return new_admin
