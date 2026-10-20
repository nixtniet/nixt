# This file is placed in the Public Domain.


"tables"


CORE = {
    "booting": "7b0049daf8ac9c541759e849dbab6ebf",
    "clients": "3b510081849e5bc4417b8f13bec66fcd",
    "command": "0a8e4a406efb5ece89b3c6ac05aae370",
    "configs": "cd3a6bfd128bcee5a8a34a7dca7a94c6",
    "default": "6da7a299d30b1f703714c4ec3a43041a",
    "defines": "e9a80e7357b02bb9eff61be27bd97f3d",
    "encoder": "92abad042c1efdf77a6cedb20c482f53",
    "excepts": "4f37c69852e5d51aacfc0ab0ffab1df1",
    "handler": "ce2669417c97854896fad10446923423",
    "looping": "ca59722b4b2a188bda75cbcc10abae78",
    "message": "7ae0c4896b3fc915cfe0fd39cf10a318",
    "methods": "5563fb8e308909d3efd27d2a07f1f432",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "5ba5d8c315f99f210d50bb547ec3191c",
    "persist": "4a94edc3d83e29e909278bf2104285a8",
    "pooling": "76c57d81410b074f47593430e566a4b8",
    "repeats": "31c1498ba4eb490a9dedcab4b0aec52c",
    "require": "169511e608fdb20d2dd9b77ebc0f25cf",
    "runtime": "e549ee7cb360d1d285d49d8212b07547",
    "tasking": "bebdedd62e611d13458cdaf917201988",
    "typings": "77251d50b6ecc33356ce5cbdde603abd",
    "utility": "d549d8d3174804992aa2947719b22d97",
    "watcher": "585dcad0f6d88c4b7db32e10dcbc9c9d"
}


MODULES = {
    "cfg": "1befdb8f5e4cd12d639d737cd8bf2233",
    "fnd": "4c972ae2d620facc199948d3aeab6f46",
    "irc": "391b76b86f17b1955a7458dba9126e6e",
    "rss": "e77ee0c512d8eb5186577d73284aba93",
    "thr": "1bd45e35978ba7b978ecacd409351fbe",
    "upt": "a3a082517a3099b155e798a9d4be0cf8",
    "ver": "f7b60ee98f308d797b36be302f01e9f6"
}


NAMES = {
    "atr": "rss",
    "cfg": "cfg",
    "dpl": "rss",
    "exp": "rss",
    "fnd": "fnd",
    "imp": "rss",
    "nme": "rss",
    "pwd": "irc",
    "rem": "rss",
    "res": "rss",
    "rss": "rss",
    "syn": "rss",
    "thr": "thr",
    "upt": "upt",
    "ver": "ver"
}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
