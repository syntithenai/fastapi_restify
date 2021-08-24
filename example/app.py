from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sys
import os  
import asyncio      
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Query, FastAPI, Request, WebSocket, WebSocketDisconnect
from typing import Optional
# development
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")
# prod
# import fastapi-mongo-restify 
from jwt_bearer import JWTBearer
from admin_router import router as AdminRouter
from restful_router import get_router
from restful_app import get_app

# products save to file

# from websocket_handler import websocket_handler         

from products_model_file import products_model

from orders_model_mongo import orders_model

token_listener = JWTBearer()  # require login for orders endpoints
app = get_app(models = {'products':products_model, 'orders':orders_model}, dependancies = {'orders':[Depends(token_listener)]}, cors_origins = ["*"], serve_admin_prefix="/admin")
# return app

# app = asyncio.run(do_get_app())

