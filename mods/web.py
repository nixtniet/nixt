# This file is placed in the Public Domain.
# pylint: disable=C0103,R0903


"web server"


import logging
import os
import sys
import time


from http.server import HTTPServer, BaseHTTPRequestHandler


from nixt.runtime import Cfg
from nixt.objects import Object
from nixt.threads import launch
from nixt.utility import where


def init():
    "initialze web server."
    Config.path = os.path.join(where(Object), "nucleus")
    if not os.path.exists(os.path.join(Config.path, 'index.html')):
        logging.warning("no index.html")
        return None
    try:
        server = HTTP((Config.hostname, int(Config.port)), HTTPHandler)
        server.start()
        logging.warning("http://%s:%s", Config.hostname, Config.port)
        return server
    except OSError as ex:
        logging.warning("%s", str(ex))
    return None

class Config:

    """Config"""

    debug = False
    hostname = "localhost"
    path = ""
    port = 8000


class HTTP(HTTPServer, Object):

    """HTTP"""

    daemon_thread = True
    allow_reuse_address = True

    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        Object.__init__(self)
        self.host = args[0]
        self._starttime = time.time()
        self._last = time.time()
        self._status = "start"

    def exit(self):
        "stop web server."
        time.sleep(0.2)
        self._status = ""
        self.shutdown()

    def start(self):
        "starts web server."
        launch(self.serve_forever)
        self._status = "ok"

    def request(self):
        "record time of last request."
        self._last = time.time()

    def error(self, _request, _addr):
        "log error."
        exctype, excvalue, _trb = sys.exc_info()
        exc = exctype(excvalue)
        logging.exception(exc)


class HTTPHandler(BaseHTTPRequestHandler):

    """HTTPHandler"""

    def setup(self):
        "setup reqeust handler."
        BaseHTTPRequestHandler.setup(self)
        self._size = 0
        self._ip = self.client_address[0]

    def raw(self, data):
        "send raw data on the socket."
        self.wfile.write(data)

    def send(self, txt):
        "send text over the socket."
        self.wfile.write(bytes(txt, encoding="utf-8"))
        self.wfile.flush()

    def write_header(self, htype='text/plain', size=None):
        "write header."
        self.send_response(200)
        self.send_header('Content-type', f'{htype}; charset="utf-8"')
        #self.send_header('Content-type', '%s;')
        if size is not None:
            self.send_header('Content-length', size)
        self.send_header('Server', "1")
        self.end_headers()

    def log(self, code):
        "log eror code."

    def do_GET(self):
        "perform a get operation."
        if "favicon" in self.path:
            return
        if Cfg.debug:
            return
        if self.path == "/":
            path = "index.html"
        else:
            path = self.path
        path = Config.path + os.sep + path
        if not os.path.exists(path):
            self.write_header("text/html")
            self.send_response(404)
            self.end_headers()
            return
        if "_images" in path:
            try:
                with open(path, "rb") as file:
                    img = file.read()
                    file.close()
                ext = self.path[-3]
                self.write_header(f"image/{ext}", len(img))
                self.raw(img)
            except (TypeError, FileNotFoundError, IsADirectoryError):
                self.send_response(404)
                self.end_headers()
            return
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                txt = file.read()
                file.close()
            self.write_header("text/html")
            self.send(txt)
        except (TypeError, FileNotFoundError, IsADirectoryError):
            self.send_response(404)
            self.end_headers()


def html2(txt):
    "wrap text in html." 
    return f"""<!doctype html>
<html>
   {txt}
</html>
"""
