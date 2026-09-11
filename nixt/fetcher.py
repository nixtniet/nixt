# This file is placed in the Public Domain.


"fetching feeds"


import html
import re
import urllib
import urllib.error
import urllib.parse
import urllib.request


from typing import ClassVar


from .methods import Method
from .objects import Data


class Fetcher:

    "fetch urls"

    modified: ClassVar[dict[str,str]] = {}

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
        url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
        req = urllib.request.Request(str(url))
        req.add_header("User-Agent", cls.useragent("RSS Fetcher"))
        since = cls.modified.get(url, "")
        if since:
            req.add_header('If-Modified-Since', since)
        response = Data()
        response.reason = ""
        try:
            Method.update(response, cls.request(req))
        except ValueError as ex:
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
    def request(cls, req):
        with urllib.request.urlopen(req, timeout=4) as response:  # nosec
            modi = response.headers.get('Last-Modified', "")
            if modi:
                cls.modified[req.get_full_url()] = modi
            response.data = response.read()
            response.error = ""
            return response

    @classmethod
    def striphtml(cls, text):
        "strip html."
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    @classmethod
    def unescape(cls, text):
        "unescape html."
        txt = re.sub(r"\s+", " ", text)
        return html.unescape(txt)

    @classmethod
    def unquote(cls, url):
        "unquote an url."
        return urllib.parse.unquote(url, errors='ignore')

    @classmethod
    def useragent(cls, txt):
        "produce useragent string."
        return "Mozilla/5.0 (X11; Linux x86_64) " + txt


def __dir__():
    return (
        'Fetcher',
    )
