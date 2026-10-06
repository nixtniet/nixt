# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "946a1b52fa8203d72137ec15fb68aea7",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "f0c0ff3060a620257f9df22fc9787fb7",
    "command": "aa2382b6a438f64de987b4e80b8dcbf9",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "c37c72017779a1ad15d3b94e1257c0b7",
    "defines": "039ef962a862febc0153a663e18201d9",
    "display": "d9ca926a5cf3173d0bc758bc254003c5",
    "encoder": "0c98563c401e13346c1ec43515f4bc64",
    "fetcher": "e780e5a4edba5b5ef03b697a7206b33c",
    "handler": "a569b4df084e1a35798cb135555ae3d6",
    "loggers": "dd73bcbf4004f5a33d15156742b235e8",
    "looping": "6f8666579aec275d965035864833f797",
    "message": "7cc5255ed84908310753a8d305831f61",
    "methods": "4a5d87f4d70f5335f58f8ef60720635a",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "855a1716ed970848ef4cd035d26dac74",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "6deceebeb0702f57bfbd9d0eaf1cd775",
    "pooling": "f4323daad55e86892317acb7abcbda7d",
    "repeats": "4c3627f380217e44f000c4498991521a",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "1d72b7273cf1b3a7a698c3328389c8e4",
    "runtime": "61c293d71ca3e95a37c38de53c1dcfd3",
    "sources": "d1c088f00a70866a762f660bd29b01de",
    "threads": "812bc64a6536552137ccfa2177faf8db",
    "typings": "2832b71930637c312853548880fb763c",
    "utility": "2d4291520524811c0c64c91f0c6f9623",
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
