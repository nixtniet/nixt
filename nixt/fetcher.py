# This file is placed in the Public Domain.


"fetching feeds"


import html
import re


from typing import Any, ClassVar, Dict, Union


from urllib.error   import HTTPError, URLError
from urllib.parse   import unquote, urlparse, urlunparse
from urllib.request import Request, urlopen


from .methods import Method
from .objects import Data


class Response(Data):

    def __init__(self):
        Data.__init__(self)
        self.data: bytes = b""
        self.reason: str = ""
        self.status: Union[int, None] = None


class Fetcher:

    "fetch urls"

    modified: ClassVar[Dict[str, str]] = {}

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
        response.reason = ""
        try:
            Method.update(response, cls.request(req))
        except HTTPError as ex:
            response.data = b""
            response.reason = str(ex.reason)
            response.status = ex.status
        except URLError as ex:
            response.reason = str(ex.reason)
        return response

    @classmethod
    def request(cls, req: Request) -> Dict[str, Any]:
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
