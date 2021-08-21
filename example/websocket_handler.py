import asyncio
from typing import Optional
from fastapi import Query, FastAPI, Request, WebSocket, WebSocketDisconnect


async def websocket_handler(websocket: WebSocket, clientId: Optional[int] = None):
   
    
    while True:
        try:
            await websocket.accept()
            print(f"connected to client {clientId}")
            # stream audio stats to client
            # sa = asyncio.create_task(send_audio_stats(websocket, self.get_audio_stats))
            # # create output queue and output task
            # wo = asyncio.create_task(self.sm.start_output_websocket(websocket, clientId))
            # # create input queue
            # wi = asyncio.create_task(self.sm.start_input_websocket(websocket,clientId))
            # print(f"QUERY {client}")
            
            # await websocket.send_text('hithere first')
            # try:
            while True:
                try:
                    data = await websocket.receive()
                    # print(type(data.get('bytes')))
                    # print(data.get('bytes') is not None)
                    if data.get('type') == "websocket.receive":
                        if data.get('bytes') is not None:
                            # await self.sm.handle_websocket_audio_message(clientId,data.get('bytes'))
                        elif data.get('text') is not None:
                            print(f"WS TEXT MSG: {data.get('text')}")
                except RuntimeError:
                    print('ERR: receiving data from WS')
                    #break            
                    raise WebSocketDisconnect()
                    # await asyncio.sleep(1)
          # except Exception as e:
                # print(e)
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
        except WebSocketDisconnect:
            print('CLOSE WS CONNECT CIENT')
            # await self.sm.stop_input_websocket(clientId)
            # await self.sm.stop_output_websocket(clientId)
 
