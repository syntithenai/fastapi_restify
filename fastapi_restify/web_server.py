from multiprocessing import Process
import uvicorn
import asyncio
import time
import contextlib

from uvicorn import Config, Server
from uvicorn_server_context import UvicornServerContext


import json
import os

class WebServer:
    server = None
    app = None
    proc = None
    task = None
    
    def __init__(self,app):
        self.app = app
    
    def create_server(self):
        config = Config(app=self.app, port = int(os.environ.get('PORT', '8081')), host="0.0.0.0")
        server = UvicornServerContext(config)
        return server
        
    def run(self):
        server = self.create_server()
        server.run()
   
    def __enter__(self):
        self.proc = Process(target=self.run, args=[], daemon=True)
        self.proc.start() 
        time.sleep(0.3)
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.proc.kill() # Cleanup after test
        
    async def asyncio_run(self):
        self.server = self.create_server()
        await self.server.serve()
    
    async def __aenter__(self):
        self.task = asyncio.create_task(self.asyncio_run())
        await asyncio.sleep(0.3)
        
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.server.shutdown()
        await asyncio.sleep(0.3)
        self.task.cancel() # Cleanup after test
 
