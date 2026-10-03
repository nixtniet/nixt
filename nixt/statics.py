# This file is placed in the Public Domain.


"tables"


from .typings import Dict


Hash = Dict[str, str]


CORE: Hash = {
    "booting": "31f4d8fc84d510ad31919900092e8d08",
    "brokers": "0628a05c07344781c68dead71a083f78",
    "buffers": "20e3a0813ebc95cffdb7cea70d5a9311",
    "clients": "bb0d56f37316fe77a70ecf44b81c0e23",
    "command": "582818a9ccc71457cbb353420075a091",
    "configs": "0563aed700fa6901b7813e8773739cbb",
    "defines": "b909644bb690c9c6f4f68389317bb57d",
    "display": "fbd0dcc5d4a7daba9ab58540dfafd14e",
    "encoder": "0c78c48615712c270896710b1fc94979",
    "engines": "d876b24a4572f94acb59d6813f0800e2",
    "fetcher": "f52653bd7659d376bd481e661a1846c8",
    "loggers": "6f03450c75c7cdf69293e58df37deca3",
    "looping": "63a5dcfb9397ed3dcb027aebb877837f",
    "message": "0db8f98189723f4be87f9d8cff1c4a48",
    "methods": "b47fb7181cee7323e271c5992f5c2eb7",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "92301c5c59aad40f01ce7491e581164e",
    "parsers": "1b032844c15e7f61d8ea4bc5d8864d8d",
    "persist": "68491e815d103fdd94b633e9f5eefb3a",
    "pooling": "0cdbf2fbf46cb6e42b31fe08ecca4a41",
    "repeats": "d99198e52b909c8fadd98f7b2bab7755",
    "require": "ef49134dcabd236d063fcbec76ee3625",
    "runners": "33db993b1f1caa067aae298e672d6cfa",
    "runtime": "e6c049f5d0c415537b29b1ae2b0cf452",
    "sources": "98dddb3d2451ff00ad445bb8e09f588a",
    "threads": "cb75bda12dfa430ecd011da80c2083c3",
    "typings": "08889217a61a1115637d5ea9f92c5008",
    "utility": "2d4291520524811c0c64c91f0c6f9623",
    "watcher": "08a77fca02b60d1c4aee81c84cb4808a"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
