# This file is placed in the Public Domain.


"tables"


from typing import Dict


CORE: Dict[str, str] = {
    "booting": "40940e37098161e0af63f948c66ed0ef",
    "brokers": "38fb6a364d4d67058844cd16fb6ec9e6",
    "buffers": "3b01fb682eb5e1afd953d8d4d997e76a",
    "clients": "8abae807251948d6cf549c561d9ee2b5",
    "command": "fe50d6b4eaeeb331fe8895b48090a516",
    "configs": "9545a7bd63d262e62f85cbb07a4a86dc",
    "defines": "344c229a317c1ce7a81c86d344860aa7",
    "display": "a920ea1b9a89aaa3d8fd025a3b5bb069",
    "encoder": "672dfad399c7d2f9171d8fa43aca4a93",
    "engines": "ff2eef46287fe19dfaa1c3f6aadb262f",
    "fetcher": "aa62315f550e02a16c14930ec54254d9",
    "loggers": "a247909a266b7fe54f1092704f1a267b",
    "looping": "6d50c69f69458950f1a46119ba9e3a7b",
    "message": "0eba074529196d479a63abd9487891fc",
    "methods": "ba19ce704e7f071ab2e94d07597382c4",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "ff991fb5249a49f9fc54b4eee653bbec",
    "parsers": "ae1107d7d4596f292752f3bf0bcad27f",
    "persist": "b8a51a9105d0523083895af09cb5bc53",
    "pooling": "bc52696b2408b20178118120327b9c1f",
    "repeats": "cfdb4d001f1b23305019f5c441ef96d9",
    "require": "15d90e6589d7892292d44e6a7d795ae6",
    "runners": "34c70ccfaf1319b55f15e1636b2ab615",
    "runtime": "65990be146767bcf349cc5526395da01",
    "sources": "bf5be27cab1a738a9d66653ad6623460",
    "threads": "aded8caf8608ab4ddcf3bbb03b91c7a8",
    "timings": "5007232b698ed4effbb35eb6f512d169",
    "utility": "9be78a01bba11615fa8266560ced6f29",
    "watcher": "58c8d20ed8c66848eddccfd5b8b62b7e"
}


MODULES: Dict[str, str] = {}


NAMES: Dict[str, str] = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
