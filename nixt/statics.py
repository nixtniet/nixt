# This file is placed in the Public Domain.


"tables"


from typing import Dict


CORE: Dict[str, str] = {
    "booting": "40940e37098161e0af63f948c66ed0ef",
    "brokers": "38fb6a364d4d67058844cd16fb6ec9e6",
    "buffers": "20e3a0813ebc95cffdb7cea70d5a9311",
    "clients": "de54fdc0d1d46e36adaca48df6381078",
    "command": "dd7a654deb482e09e2fbe9c119c880dd",
    "configs": "9545a7bd63d262e62f85cbb07a4a86dc",
    "defines": "344c229a317c1ce7a81c86d344860aa7",
    "display": "fbd0dcc5d4a7daba9ab58540dfafd14e",
    "encoder": "672dfad399c7d2f9171d8fa43aca4a93",
    "engines": "e573c989ec9c03f0973c75e66fac79e6",
    "fetcher": "aa62315f550e02a16c14930ec54254d9",
    "loggers": "a1d0f49b0f90fad9042bb0a4baf0ece5",
    "looping": "3984123bce23fe6b8f3d3dad2eea449b",
    "message": "12fb96d2d5703a39c6d47364b5575eab",
    "methods": "ba19ce704e7f071ab2e94d07597382c4",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "ff991fb5249a49f9fc54b4eee653bbec",
    "parsers": "ae1107d7d4596f292752f3bf0bcad27f",
    "persist": "b8a51a9105d0523083895af09cb5bc53",
    "pooling": "bc52696b2408b20178118120327b9c1f",
    "repeats": "cfdb4d001f1b23305019f5c441ef96d9",
    "require": "9b1bc83c03919ad244f6c17568f75c17",
    "runners": "34c70ccfaf1319b55f15e1636b2ab615",
    "runtime": "7970db9f8e20240ef59834f4cb6e0773",
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
