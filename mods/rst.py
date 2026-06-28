# This file is placed in the Public Domain.


"rest server"


import logging
import os
import sys
import time


from http.server import HTTPServer, BaseHTTPRequestHandler


from nixt.defines import Object, Locate, Main, Thread, Workdir


def init():
    "initialize the rest module."
    try:
        rest = REST((Config.hostname, int(Config.port)), RESTHandler)
        rest.start()
        logging.warning("http://%s:%s", Config.hostname, Config.port)
        return rest
    except OSError as ex:
        logging.error(str(ex))


class Config(Object):

    hostname = "localhost"
    port = 10102


class REST(HTTPServer, Object):

    allow_reuse_address = True
    daemon_thread = True

    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        Object.__init__(self)
        self.host = args[0]
        self._last = time.time()
        self._starttime = time.time()
        self._status = "start"

    def request(self):
        "handle request."
        self._last = time.time()

    def error(self, _request, _addr):
        "log error."
        exctype, excvalue, _trb = sys.exc_info()
        exc = exctype(excvalue)
        logging.exception(exc)

    def exit(self):
        "exit rest server."
        self._status = ""
        time.sleep(0.2)
        self.shutdown()

    def start(self):
        "start rest server."
        Locate.first(Config)
        self._status = "ok"
        Thread.launch(self.serve_forever)


class RESTHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        "handle get request."
        if Main.debug:
            return
        if "favicon" in self.path:
            return
        if self.path == "/":
            self.write_header("text/html")
            txt = ""
            for fnm in Workdir.kinds():
                hn = Config.hostname
                port = Config.port
                txt += f'<a href="http://{hn}:{port}/{fnm}">{fnm}</a><br>\n'
            self.send(self.html(txt.strip()))
            return
        if self.path.startswith("/"):
            fnm = self.path[1:]
        else:
            fnm = self.path
        fnm = os.path.join(Workdir.wdr, "store", fnm)
        fnm = os.path.abspath(fnm)
        if os.path.isdir(fnm):
            self.write_header("text/html")
            txt = ""
            for fnn in os.listdir(fnm):
                fn = self.path + os.sep + fnn
                hn = Config.hostname
                port = Config.port
                txt += f'<a href="http://{hn}:{port}/{fn}">{fn}</a><br>\n'
            self.send(txt.strip())
            return
        try:
            with open(fnm, "r", encoding="utf-8") as file:
                txt = file.read()
                file.close()
            self.write_header("text/html")
            self.send(self.html(txt))
        except (TypeError, FileNotFoundError, IsADirectoryError) as ex:
            self.send_response(404)
            logging.debug(str(ex))
            self.end_headers()

    def html(self, text):
        "wrap text as html."
        return """<!doctype html>\n<html>   %s\n</html>""" % text

    def log(self, code):
        "log some."

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self._ip = self.client_address[0]
        self._size = 0

    def send(self, txt):
        "send text to socket."
        self.wfile.write(bytes(txt, "utf-8"))
        self.wfile.flush()

    def write_header(self, htype='text/plain'):
        "write header to socket."
        self.send_response(200)
        self.send_header('Content-type', '%s; charset=%s ' % (htype, "utf-8"))
        self.send_header('Server', "1")
        self.end_headers()
