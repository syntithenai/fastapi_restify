import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/fastapi-mongo-restify")

from web_server import WebServer
from app import app

# import uvicorn

if __name__ == '__main__':
    
    async def doit():
        with WebServer(app):
            while True:
                await asyncio.sleep(0.1)
    # uvicorn.run('app:app', host="0.0.0.0", port=8080, reload=True)
    asyncio.run(doit())
