# This file is placed in the Public Domain.


"fetching feeds"


import html
import re
import urllib
import urllib.error
import urllib.parse
import urllib.request


from typing import ClassVar, Dict, TextIO


from urllib.parse import unquote, urlparse, urlunparse
from urllib.request import Request, urlopen


from .methods import Method
from .objects import Data


class Fetcher:

    "fetch urls"

    modified: ClassVar[Dict[str,str]] = {}

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
    def geturl(cls, url: str) -> Data:
        "fetch an url."
        url = urlunparse(urlparse(url))
        req = Request(str(url))
        req.add_header("User-Agent", cls.useragent("RSS Fetcher"))
        since = cls.modified.get(url, "")
        if since:
            req.add_header('If-Modified-Since', since)
        response = Data()
        response.reason = ""
        try:
            Method.update(response, cls.request(req))
        except Exception as ex:
            response.data = b""
            try:
                response.reason = ex.reason
            except AttributeError:
                response.reason = str(ex)
            try:
                response.status = ex.status
            except AttributeError:
                response.status = 0
        return response

    @classmethod
    def request(cls, req: Request) -> TextIO:
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
    def unquote(cls, url) -> str:
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
