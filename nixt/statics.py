# This file is placed in the Public Domain.


"tables"


from typing import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "946a1b52fa8203d72137ec15fb68aea7",
    "brokers": "be3138aaf29cd7bbe2469ae71269647f",
    "buffers": "f0c0ff3060a620257f9df22fc9787fb7",
    "command": "129234a5e166be2afc6b19fd2fbdebe8",
    "configs": "915a02e10b32cc61a5365e6401876008",
    "default": "6e261ecbd6e9ae42ce133a13b3a2b81d",
    "defines": "039ef962a862febc0153a663e18201d9",
    "display": "f96dfc3e3d0a9527d2172b34e9207ff1",
    "encoder": "0c98563c401e13346c1ec43515f4bc64",
    "fetcher": "a98c4c3d790e9dc2b7531074038e2b6d",
    "handler": "b6bbae1b8e962c1023742ae55325aa7f",
    "loggers": "dd73bcbf4004f5a33d15156742b235e8",
    "looping": "6f8666579aec275d965035864833f797",
    "message": "8aed09bc218f089f756e42cccfcc36c0",
    "methods": "b24a809698acdc68e66365ee7169ec9b",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "b5f7dec775b8c9a6009efd31738bf622",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "dbf05305d4c5fa716d046ad9f9bd609a",
    "pooling": "9a001965a4e17a82c12bed1b3661fa9a",
    "repeats": "4c3627f380217e44f000c4498991521a",
    "require": "64863daa33090e4956eef461fd06280c",
    "runners": "1d72b7273cf1b3a7a698c3328389c8e4",
    "runtime": "133167a80848ccabe0534fe8cf86145c",
    "sources": "c9ee3a48be447f97db87e00b291d61c0",
    "threads": "d59cb461458e1a6ff80a4b628bf4b2b1",
    "typings": "1a7ae589e7e9f3e0a320e8353d76178b",
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
