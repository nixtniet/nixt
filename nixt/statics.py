# This file is placed in the Public Domain.


"tables"


from typing import Dict


CORE: Dict[str, str] = {
    "booting": "40940e37098161e0af63f948c66ed0ef",
    "brokers": "38fb6a364d4d67058844cd16fb6ec9e6",
    "buffers": "f80d0c0f235906b32e119c0f28732f53",
    "clients": "0b7a52d0c0faf4299a4b02d877399166",
    "command": "034fb51b228d3d457b13bb63fc2593bc",
    "configs": "b03f330521d09d5b47114619c58bcafd",
    "defines": "66421075f718dd5bdd0dc5f2cdcf13c1",
    "display": "8cee17e61f2b0e1b2cf017dbc6dc511c",
    "encoder": "672dfad399c7d2f9171d8fa43aca4a93",
    "engines": "c2960c54d18912e1906d9c8956467f39",
    "fetcher": "5c1ecd8df79ce17c7ad87d5dbf8aa9e1",
    "loggers": "a247909a266b7fe54f1092704f1a267b",
    "looping": "7e7aeca78f3e192a25e8dce33b7544fa",
    "message": "b74f39d0992d98e222dbf14c2da04516",
    "methods": "ba19ce704e7f071ab2e94d07597382c4",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "ff991fb5249a49f9fc54b4eee653bbec",
    "parsers": "ae1107d7d4596f292752f3bf0bcad27f",
    "persist": "b8a51a9105d0523083895af09cb5bc53",
    "pooling": "bc52696b2408b20178118120327b9c1f",
    "repeats": "cfdb4d001f1b23305019f5c441ef96d9",
    "require": "892e5f99d4282a489f890bf1e8a52ce3",
    "runners": "34c70ccfaf1319b55f15e1636b2ab615",
    "runtime": "eceac157fedcb23fd8489466ab80e318",
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
