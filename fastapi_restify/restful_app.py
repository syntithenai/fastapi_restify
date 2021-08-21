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


def get_app(models, dependancies = None, serve_static_prefix = None, serve_admin_prefix = None, cors_origins = None, ws_handler = None):
    
    stage = os.environ.get('STAGE', None)
    openapi_prefix = f"/{stage}" if stage else "/"
    app = FastAPI(openapi_prefix=openapi_prefix)
    token_listener = JWTBearer()
        
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
        # login
        app.include_router(AdminRouter, tags=["Login"], prefix=serve_admin_prefix)

    if ws_handler is not None:
        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket, clientId: Optional[int] = None):
            await ws_handler(websocket, clientId)
            # EXAMPLE HANDLER
            # async def send_audio_stats(websocket, stats):
                # while True:
                    # try:
                        # # await websocket.send_text('audio stats')
                        # await websocket.send_json(stats())
                    # except:
                        # pass
                        # # print('send audio stats')
                    # await asyncio.sleep(0.1)
            
            # while True:
                # try:
                    # await websocket.accept()
                    # print(f"connected to client {clientId}")
                    # # stream audio stats to client
                    # sa = asyncio.create_task(send_audio_stats(websocket, self.get_audio_stats))
                    # # create output queue and output task
                    # wo = asyncio.create_task(self.sm.start_output_websocket(websocket, clientId))
                    # # create input queue
                    # wi = asyncio.create_task(self.sm.start_input_websocket(websocket,clientId))
                    # # print(f"QUERY {client}")
                    
                    # # await websocket.send_text('hithere first')
                    # # try:
                    # while True:
                        # try:
                            # data = await websocket.receive()
                            # # print(type(data.get('bytes')))
                            # # print(data.get('bytes') is not None)
                            # if data.get('type') == "websocket.receive":
                                # if data.get('bytes') is not None:
                                    # await self.sm.handle_websocket_audio_message(clientId,data.get('bytes'))
                                # elif data.get('text') is not None:
                                    # print(f"WS TEXT MSG: {data.get('text')}")
                        # except RuntimeError:
                            # print('ERR: receiving data from WS')
                            # #break            
                            # raise WebSocketDisconnect()
                            # # await asyncio.sleep(1)
                  # # except Exception as e:
                        # # print(e)
                    # try:
                        # sa.cancel()
                    # except asyncio.CancelledError:
                        # pass
                    # try:
                        # wi.cancel()
                    # except asyncio.CancelledError:
                        # pass
                    # try:
                        # wo.cancel()
                    # except asyncio.CancelledError:
                        # pass
                # except WebSocketDisconnect:
                    # print('CLOSE WS CONNECT CIENT')
                    # await self.sm.stop_input_websocket(clientId)
                    # await self.sm.stop_output_websocket(clientId)
                    


    assign_restful_routes(app,models, dependancies)
    return app
