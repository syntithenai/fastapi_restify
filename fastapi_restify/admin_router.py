from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
import sys
import os
from decouple import config
import motor.motor_asyncio
from bson import ObjectId
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )
from response_models import *
from admin_model import AdminModel
from jwt_handler import signJWT

admin_collection = None

async def get_collection():
    # if admin_collection is None:
    mongo_uri = config('MONGO_URI')
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
    database = client[config('MONGO_DATABASE')]
    admin_collection = database.get_collection('admin_users')
    return admin_collection
    # else: 
        # return admin_collection
    

async def add_admin(admin_data: dict) -> dict:
    admin_collection = await get_collection()
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
    admin_collection = await get_collection()
    admin_user = await admin_collection.find_one({"email": admin_credentials.username}, {"_id": 0})
    if (admin_user):
        password = hash_helper.verify(
            admin_credentials.password, admin_user["password"])
        if (password):
            token = signJWT(admin_credentials.username)
            admin_user['token'] = {'access_token': token.get("access_token")}
            return admin_user
            # return signJWT(admin_credentials.username)
        return ErrorResponseModel("Incorrect email or password",401,"Incorrect email or password")
    return ErrorResponseModel("Incorrect email or password",401,"Incorrect email or password")

@router.post("/create_user")
async def admin_signup(admin: AdminModel = Body(...)):
    admin_collection = await get_collection()
    admin_exists = await admin_collection.find_one({"email":  admin.email}, {"_id": 0})
    if(admin_exists):
        return ErrorResponseModel("Email already exists",403,"Email already exists")
    if admin.password != admin.password2:
        return ErrorResponseModel("Passwords do not match",403,"Passwords do not match")
    else:
        admin.password = hash_helper.encrypt(admin.password)
        admin.password2 = None
        new_admin = await add_admin(jsonable_encoder(admin))
        return new_admin
