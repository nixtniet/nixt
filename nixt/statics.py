# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "d7d8495daba0045c375698b52003acfa",
    "brokers": "35a302a66ba8cbfc195edab4f21727af",
    "buffers": "4111f8c0b76d46b8a233f158d86dd57d",
    "clients": "0acf656025ea6389f1c7b69673f267d3",
    "command": "93f4d99a6adc7579b99dbf03ec5f1885",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "0cf7aa1b97a025175262e3c252a93e8e",
    "defines": "86bc20bc402bece5603450d563c4addf",
    "display": "ac31f93aa65333f93c8a481e55f20ffd",
    "encoder": "0c98563c401e13346c1ec43515f4bc64",
    "example": "9572f920d655315cebfc46261e1e63f1",
    "fetcher": "e780e5a4edba5b5ef03b697a7206b33c",
    "fqueues": "a08f99bd7a12659346395afc461d3cc0",
    "handler": "d3cd121f1fa4a2e593421821a8a67b30",
    "loggers": "dd73bcbf4004f5a33d15156742b235e8",
    "looping": "6f8666579aec275d965035864833f797",
    "message": "7cc5255ed84908310753a8d305831f61",
    "methods": "9348e9bb7c9e180db8dce8671cfc0eb3",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "outputs": "6b07a747b979eda27697c8fc53619b08",
    "package": "855a1716ed970848ef4cd035d26dac74",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "6deceebeb0702f57bfbd9d0eaf1cd775",
    "pooling": "f4323daad55e86892317acb7abcbda7d",
    "repeats": "4c3627f380217e44f000c4498991521a",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "1d72b7273cf1b3a7a698c3328389c8e4",
    "runtime": "61c293d71ca3e95a37c38de53c1dcfd3",
    "screens": "3b93e3d317fa201b293badde87dec770",
    "sources": "d1c088f00a70866a762f660bd29b01de",
    "threads": "812bc64a6536552137ccfa2177faf8db",
    "timings": "1b364da5410297c9deecacfe972c0431",
    "typings": "138b5c9ef0b86dbe0d27ec518a6408f5",
    "utility": "85d0b075e6466707602b1baea97f8a93",
    "watcher": "f3934ed62a06b75338e0454d7219fd39"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
