# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "ec241ffb0f7e481a79974f363fc204ea",
    "brokers": "35a302a66ba8cbfc195edab4f21727af",
    "buffers": "4111f8c0b76d46b8a233f158d86dd57d",
    "clients": "0acf656025ea6389f1c7b69673f267d3",
    "command": "108bc1c21569b5227535e14cdddf6763",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "848ab4b6f4eafdfcda31cba7311d62fa",
    "defines": "2df7490677b2d210fe58c6bcafa13153",
    "display": "81878eeec837b01ec4ef431b9b6ca7a8",
    "dqueues": "9c61cf716ca3e9b49c0c19669af53fca",
    "encoder": "a3812b8a3463e33bc8fc1db9ae7aac53",
    "excepts": "4bfa36a4765b270a29c8c71f3ac1b108",
    "fetcher": "5dc6fd7d6b0410adbee0b43b216bf2bd",
    "handler": "4a25a67e8b516fa25f3b4b1d07e54992",
    "loggers": "27c867484e3cca8cff53584f1a514eb9",
    "looping": "8db40d67d96c02d092cb4cfbf6da99ca",
    "message": "07e8febe6e1e5e2170a518d9826879c2",
    "methods": "4bb771a2dc9b1893907f02c2aa53617e",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "outputs": "5c26daa37877213a72d14ef4878410b6",
    "package": "1098af502dcde8586901fef49761f4b0",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "05e98937fa8629f7420dcbcb84e69e39",
    "pooling": "3aef2f8677df380f8aa7d2b1bb715d0c",
    "repeats": "71fb58b59d46577ae59dbcd570ce4028",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "ad38cfe20ee364a9b61613a78ce3177b",
    "runtime": "61c293d71ca3e95a37c38de53c1dcfd3",
    "screens": "3b93e3d317fa201b293badde87dec770",
    "sources": "b62e6c4520d84458618ab52f1b2985e5",
    "tasking": "1ebffb8594f0f424f4ff83ecbc2c8a72",
    "timings": "1b364da5410297c9deecacfe972c0431",
    "typings": "8674b7118e042709e5b88692a7945a76",
    "utility": "9b4d19f3f73774ee053d27f2c5a590e1",
    "watcher": "24434817f9ef07676ba93a77458c1949"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
