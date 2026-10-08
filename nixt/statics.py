# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "ec241ffb0f7e481a79974f363fc204ea",
    "brokers": "35a302a66ba8cbfc195edab4f21727af",
    "buffers": "4111f8c0b76d46b8a233f158d86dd57d",
    "clients": "0acf656025ea6389f1c7b69673f267d3",
    "command": "93f4d99a6adc7579b99dbf03ec5f1885",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "2a6879c304a1b661fd69154cbc0fc86a",
    "defines": "0b2ad6050832ab8d8f0ee17dcd57faaa",
    "display": "ac31f93aa65333f93c8a481e55f20ffd",
    "dqueues": "a58885d496ea20f8c1c16a05f37ee0fa",
    "encoder": "76c3d15d9554682bfece255081bab634",
    "example": "9572f920d655315cebfc46261e1e63f1",
    "fetcher": "e780e5a4edba5b5ef03b697a7206b33c",
    "handler": "40753b8b6b21ea8cde18072210859a48",
    "loggers": "979ae5d3ba7a6f60f563991c125a9e48",
    "looping": "71c9714b0b6cf17a783616b0d4b86e38",
    "message": "07e8febe6e1e5e2170a518d9826879c2",
    "methods": "64b225e2df647d3cd073ed6962507a47",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "outputs": "5c26daa37877213a72d14ef4878410b6",
    "package": "1098af502dcde8586901fef49761f4b0",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "58f2b760d3280af327e21877f377bbb9",
    "pooling": "f4323daad55e86892317acb7abcbda7d",
    "repeats": "bcb46f0f534a514c0af36dfa7b3c1a29",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "ad38cfe20ee364a9b61613a78ce3177b",
    "runtime": "61c293d71ca3e95a37c38de53c1dcfd3",
    "screens": "3b93e3d317fa201b293badde87dec770",
    "sources": "b62e6c4520d84458618ab52f1b2985e5",
    "tasking": "1ebffb8594f0f424f4ff83ecbc2c8a72",
    "timings": "1b364da5410297c9deecacfe972c0431",
    "typings": "8674b7118e042709e5b88692a7945a76",
    "utility": "85d0b075e6466707602b1baea97f8a93",
    "watcher": "36356ec9e289f1d6866f89172cdfc676"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
