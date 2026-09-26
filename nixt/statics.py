# This file is placed in the Public Domain.


"tables"


from typing import Dict


CORE: Dict[str, str] = {
    "booting": "40940e37098161e0af63f948c66ed0ef",
    "brokers": "557ed4ae519880baabfb2b5b2edcdb5f",
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
    "methods": "937f60ce4d8447d3bfd09879e88460fc",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "6a1c0f3d4b3a4338826f347edb25bb9b",
    "parsers": "ae1107d7d4596f292752f3bf0bcad27f",
    "persist": "be9f8a8dc7e012f3236addd857ef1859",
    "pooling": "bc52696b2408b20178118120327b9c1f",
    "repeats": "78e43e4280e64f0ee24f2fcc51f80446",
    "require": "892e5f99d4282a489f890bf1e8a52ce3",
    "runners": "3952b86074abe27be3c34b4d1770e1ea",
    "runtime": "91f0b497d601936cd580af4f555601e4",
    "sources": "bf5be27cab1a738a9d66653ad6623460",
    "threads": "aded8caf8608ab4ddcf3bbb03b91c7a8",
    "timings": "5f65c97d127d91af6fb8ed03abe5f34d",
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
