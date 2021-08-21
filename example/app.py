from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sys
import os        
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Query, FastAPI, Request, WebSocket, WebSocketDisconnect
from typing import Optional
# development
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")
# prod
# import fastapi-mongo-restify 
from auth.jwt_bearer import JWTBearer
from auth.admin_router import router as AdminRouter
from restful_router import get_router
from restful_app import get_app

# products save to file
from products_model_file import products_model
# orders save to mongo
from orders_model_mongo import orders_model

# from websocket_handler import websocket_handler         


token_listener = JWTBearer()  # require login for orders endpoints
app = get_app(models = {'products':products_model, 'orders':orders_model}, dependancies = {'orders':[Depends(token_listener)]}, cors_origins = ["*"])

