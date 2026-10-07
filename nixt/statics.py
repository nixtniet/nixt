# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "c72cbe16095b6df2f358d33cd78b8610",
    "brokers": "35a302a66ba8cbfc195edab4f21727af",
    "buffers": "4111f8c0b76d46b8a233f158d86dd57d",
    "clients": "0acf656025ea6389f1c7b69673f267d3",
    "command": "93f4d99a6adc7579b99dbf03ec5f1885",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "51bf4b88425895e22757d840619c9846",
    "defines": "265a815a496efc6575c5f432fd56c20f",
    "display": "ac31f93aa65333f93c8a481e55f20ffd",
    "encoder": "0c98563c401e13346c1ec43515f4bc64",
    "example": "9572f920d655315cebfc46261e1e63f1",
    "fetcher": "e780e5a4edba5b5ef03b697a7206b33c",
    "handler": "40753b8b6b21ea8cde18072210859a48",
    "jlqueue": "f83ceefeb8aa6a8504d74cfbf0933834",
    "loggers": "dd73bcbf4004f5a33d15156742b235e8",
    "looping": "c63da1fe1c26388e684da267f0f66315",
    "message": "ea599f57aac074cd169ab5adfa17c6af",
    "methods": "9348e9bb7c9e180db8dce8671cfc0eb3",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "outputs": "5c26daa37877213a72d14ef4878410b6",
    "package": "855a1716ed970848ef4cd035d26dac74",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "6deceebeb0702f57bfbd9d0eaf1cd775",
    "pooling": "f4323daad55e86892317acb7abcbda7d",
    "repeats": "bcb46f0f534a514c0af36dfa7b3c1a29",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "ad38cfe20ee364a9b61613a78ce3177b",
    "runtime": "61c293d71ca3e95a37c38de53c1dcfd3",
    "screens": "3b93e3d317fa201b293badde87dec770",
    "sources": "d1c088f00a70866a762f660bd29b01de",
    "tasking": "04408412ead4bb5d30c2b46330fca77d",
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
