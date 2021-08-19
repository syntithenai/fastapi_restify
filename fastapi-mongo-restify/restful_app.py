from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import sys
import os        
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Query, FastAPI, Request, WebSocket, WebSocketDisconnect
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")
from auth.admin_router import router as AdminRouter
from restful_router import get_router
from auth.jwt_bearer import JWTBearer

def assign_restful_routes(app, models, dependancies = None):
    for model in models:
        # rest apis
        if dependancies is not None and 'model' in dependancies:
            app.include_router(get_router(models[model]), tags=["Rest APIs"], prefix="/"+model , dependencies=dependancies[model])
        else:
            app.include_router(get_router(models[model]), tags=["Rest APIs"], prefix="/"+model )
            
    return app


def get_app(models, dependancies = None, serve_static_prefix = None, serve_admin_prefix = None, cors_origins = None):
    app = FastAPI()
    if serve_static_prefix:
        base_path = serve_static_prefix + "/web_server_resources/"
        app.mount("/static", StaticFiles(directory= base_path + "static/"), name="static")
        templates = Jinja2Templates(directory= base_path + "templates")

        @app.get("/")
        def read_root(request: Request):
            return templates.TemplateResponse("index.html", {"request": request})

    if cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
            
    if serve_admin_prefix:
        token_listener = JWTBearer()
        # login
        app.include_router(AdminRouter, tags=["Login"], prefix=serve_admin_prefix)

    assign_restful_routes(app,models, dependancies)
    return app
