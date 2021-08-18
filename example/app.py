from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
        
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# from auth.jwt_bearer import JWTBearer

from restful_router import get_router
# products save to file
from products_model_file import products_model
# orders save to mongo
from orders_model_mongo import orders_model

app = FastAPI(title='Test FastAPI Mongo Restify')
        base_path = os.path.dirname(os.path.abspath(__file__))+"/web_server_resources/"
        app.mount("/static", StaticFiles(directory= base_path + "static/"), name="static")
        templates = Jinja2Templates(directory= base_path + "templates")
        
# token_listener = JWTBearer()
@app.get("/")
        def read_root(request: Request):
            return templates.TemplateResponse("index.html", {"request": request})
            
# @app.get("/", tags=["Root"])
# async def read_root():
    # return {"message": "Welcome to this fantastic app."}

# login
# app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
# rest apis
app.include_router(get_router(products_model), tags=["Products"], prefix="/products")  # , dependencies=[Depends(token_listener)]
app.include_router(get_router(orders_model), tags=["Orders"], prefix="/orders")  # , dependencies=[Depends(token_listener)]
