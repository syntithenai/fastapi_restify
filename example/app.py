from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sys
import os        
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Query, FastAPI, Request, WebSocket, WebSocketDisconnect
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")
from auth.jwt_bearer import JWTBearer
from auth.admin_router import router as AdminRouter
from restful_router import get_router
# products save to file
from products_model_file import products_model
# orders save to mongo
from orders_model_mongo import orders_model

app = FastAPI(title='Test FastAPI Mongo Restify')

base_path = os.path.dirname(os.path.abspath(__file__))+"/web_server_resources/"
app.mount("/static", StaticFiles(directory= base_path + "static/"), name="static")
templates = Jinja2Templates(directory= base_path + "templates")
        
token_listener = JWTBearer()
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# login
app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
# rest apis
app.include_router(get_router(products_model), tags=["Products"], prefix="/products" , dependencies=[Depends(token_listener)])
app.include_router(get_router(orders_model), tags=["Orders"], prefix="/orders")  # , dependencies=[Depends(token_listener)]
