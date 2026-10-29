# This file is placed in the Public Domain.


"fetch urls"


import html
import http
import re
import urllib


from http.client    import RemoteDisconnected
from urllib.error   import HTTPError, URLError
from urllib.parse   import unquote, urlparse, urlunparse
from urllib.request import Request, urlopen


from .configs import Main
from .default import Log
from .utility import MD5


logger = Log(__name__)


class Fetcher:

    "fetch urls"

    modified = {}

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
    def fetch(cls, url):
        "fetch a feed."
        try:
            return cls.geturl(url)
        except (RemoteDisconnected, TimeoutError) as ex:
            logger.debug("%s %s", url, ex)
        except HTTPError as ex:
            if ex.status != 304:
                logger.debug("%s %s", url, ex.reason)
        except URLError as ex:
            logger.debug("%s %s", url, ex.reason)

    @classmethod
    def geturl(cls, url):
        "fetch an url."
        url = urlunparse(urlparse(url))
        req = Request(str(url))
        req.add_header("User-Agent", cls.useragent(f"{Main.name.upper()} {MD5.core()}"))
        since = cls.modified.get(url, "")
        if since:
            req.add_header('If-Modified-Since', since)
        with urlopen(req, timeout=10) as response:  # nosec
            modi = response.headers.get('Last-Modified', "")
            if modi:
                cls.modified[req.get_full_url()] = modi
            return str(response.read(), "utf-8", errors='ignore')

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
        return unquote(url, errors='ignore')

    @classmethod
    def useragent(cls, text):
        "produce useragent string."
        return "Mozilla/5.0 (X11; Linux x86_64) " + text


def __dir__():
    return (
        "Fetcher",
    )
