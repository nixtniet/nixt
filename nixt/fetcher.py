# This file is placed in the Public Domain.


"fetching feeds"


import html
import re


from urllib.parse   import unquote, urlparse, urlunparse
from urllib.request import Request, urlopen


from .methods import Method
from .objects import Data
from .typings import Any, ClassVar, Dict, Union


Anys = Dict[str, Any]
Integer = Union[int, None]
Strings = Dict[str, str]


class Response(Data):

    "response object"

    def __init__(self):
        Data.__init__(self)
        self.data: bytes = b""
        self.reason: str = ""
        self.status: Integer = None
        self.url: str = ""


class Fetcher:

    "fetch urls"

    modified: ClassVar[Strings] = {}

    @classmethod
    def cdata(cls, line: str) -> str:
        "scrape CDATA block."
        if "CDATA" in line:
            lne = line.replace("![CDATA[", "")
            lne = lne.replace("]]", "")
            lne = lne[1:-1]
            return lne
        return line

    @classmethod
    def geturl(cls, url: str) -> Response:
        "fetch an url."
        url = urlunparse(urlparse(url))
        req = Request(str(url))
        req.add_header("User-Agent", cls.useragent("RSS Fetcher"))
        since = cls.modified.get(url, "")
        if since:
            req.add_header('If-Modified-Since', since)
        response = Response()
        response.url = url
        response.reason = ""
        try:
            Method.update(response, cls.request(req))
        except Exception as ex:
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
    def request(cls, req: Request) -> Anys:
        "handle  a request."
        with urlopen(req, timeout=4) as response:  # nosec
            modi = response.headers.get('Last-Modified', "")
            if modi:
                cls.modified[req.get_full_url()] = modi
            response.data = response.read()
            response.error = ""
            return response

    @classmethod
    def striphtml(cls, text: str) -> str:
        "strip html."
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    @classmethod
    def unescape(cls, text: str) -> str:
        "unescape html."
        txt = re.sub(r"\s+", " ", text)
        return html.unescape(txt)

    @classmethod
    def unquote(cls, url: str) -> str:
        "unquote an url."
        return unquote(url, errors='ignore')

    @classmethod
    def useragent(cls, text: str) -> str:
        "produce useragent string."
        return "Mozilla/5.0 (X11; Linux x86_64) " + text


def __dir__():
    return (
        'Fetcher',
    )
