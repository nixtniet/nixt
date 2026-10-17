# This file is placed in the Public Domain.


"fetching feeds"


import html


from urllib.parse   import unquote, urlparse, urlunparse
from urllib.request import Request, urlopen


from .configs import Main
from .methods import Method
from .objects import Data
from .sources import MD5
from .typings import Dict


class Response(Data):

    "response object"

    def __init__(self):
        Data.__init__(self)
        self.data = b""
        self.reason = ""
        self.status = None
        self.url = ""


class Fetcher:

    "fetch urls"

    modified: Dict[str, str] = {}

    @classmethod
    def cdata(cls, line):
        "scrape CDATA block."
        if "CDATA" in line:
            lne = line.replace("![CDATA[", "")
            lne = lne.replace("]]", "")
            lne = lne[1:-1]
            return lne
        return line

    @classmethod
    def geturl(cls, url):
        "fetch an url."
        url = urlunparse(urlparse(url))
        req = Request(str(url))
        req.add_header("User-Agent", cls.useragent(f"{Main.name.upper()} {MD5.core()}"))
        since = cls.modified.get(url, "")
        if since:
            req.add_header('If-Modified-Since', since)
        response = Response()
        response.url = url
        response.reason = ""
        try:
            Method.update(response, cls.request(req))
        except Exception as ex:
            # pylint: disable=E1101
            response.data = b""
            if "reason" in dir(ex):
                response.reason = ex.reason # type: ignore
            else:
                response.reason = str(ex)
            if "status" in dir(ex):
                response.status = ex.status # type: ignore
            else:
                response.status = None
        return response

    @classmethod
    def request(cls, req):
        "handle  a request."
        with urlopen(req, timeout=4) as response:  # nosec
            modi = response.headers.get('Last-Modified', "")
            if modi:
                cls.modified[req.get_full_url()] = modi
            response.data = response.read()
            response.error = ""
            return response

    @classmethod
    def striphtml(cls, text):
        "strip html."
        import re
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    @classmethod
    def unescape(cls, text):
        "unescape html."
        import re
        txt = re.sub(r"\s+", " ", text)
        return html.unescape(txt)

    @classmethod
    def unquote(cls, url):
        "unquote an url."
        return unquote(url, errors='ignore')

    @classmethod
    def useragent(cls, text):
        "produce useragent string."
        return "Mozilla/5.0 (X11; Linux x86_64) " + text


def __dir__():
    return (
        'Fetcher',
    )
