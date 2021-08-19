import contextlib
import time
import threading
import uvicorn
import asyncio

# https://github.com/encode/uvicorn/issues/742

# provides easy to use context
# config = Config(app=app, port = os.environ.get('PORT', '8081'))
# server = UvicornServerContext(config)
        
# with server.run_in_thread():
        # while True:
            # time.sleep(1e-3)

 
class UvicornServerContext(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()
