"""Run a browser check with its own local HTTP server, then close the server."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import runpy,sys,threading
TESTS=Path(__file__).resolve().parent
if len(sys.argv)<2:
    raise SystemExit('Usage: python run_browser.py journey.py')
target=(TESTS/sys.argv[1]).resolve()
if target.parent!=TESTS or not target.is_file():
    raise SystemExit('Choose a test file in this directory.')
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(TESTS.parents[1])))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
base=f'http://127.0.0.1:{server.server_port}/neural-lab/'
if target.name=='browser.py':base+='?advanced'
sys.argv=[str(target),base]
try:runpy.run_path(str(target),run_name='__main__')
finally:server.shutdown();server.server_close()
