# This file is placed in the Public Domain.


"tables"


from .typings import Hash


CORE: Hash = {
    "booting": "032ce55a875bf6526bba9f613bd40c3c",
    "brokers": "61a90cb19c1eb2dac07f695b59ad2a42",
    "buffers": "20e3a0813ebc95cffdb7cea70d5a9311",
    "clients": "de54fdc0d1d46e36adaca48df6381078",
    "command": "4822654602881da3cdeb60604c147281",
    "configs": "9545a7bd63d262e62f85cbb07a4a86dc",
    "defines": "3327ce15cd094bc0ca209e4469c91b3a",
    "display": "fbd0dcc5d4a7daba9ab58540dfafd14e",
    "encoder": "869c8951a8c51694901ec656be197bf5",
    "engines": "d876b24a4572f94acb59d6813f0800e2",
    "fetcher": "28cd4b40e5d26c4ca4f21cffb7d21067",
    "loggers": "a247909a266b7fe54f1092704f1a267b",
    "looping": "1e9cf618f5a3e7a3734be8c87700b476",
    "message": "0db8f98189723f4be87f9d8cff1c4a48",
    "methods": "28c030ef254af4d93ce4eb914f72e2bc",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "ff991fb5249a49f9fc54b4eee653bbec",
    "parsers": "53e6f850e9ab3796016ae42d39483c4e",
    "persist": "3af53032630e5c01b1722f1f031b5d4a",
    "pooling": "0cdbf2fbf46cb6e42b31fe08ecca4a41",
    "repeats": "12ad8f5ad1c1baf37ccebd6bcb5a8837",
    "require": "e434fc25c78b1fc3d03855a6685b4aae",
    "runners": "be2d3bd48afa50d60208804e2fda1dbd",
    "runtime": "96bf1410e22eccc4cd3cddb624393aba",
    "sources": "930fb3fe293b956c47ea91d4a9ecab4a",
    "threads": "ea74bbae8b235d33889ff78c77c4ff7a",
    "typings": "69150f98ffd5f693b3f0eae53708ad7f",
    "utility": "7ee5026c8ba1de35112a68079e7bb7b4",
    "watcher": "58c8d20ed8c66848eddccfd5b8b62b7e"
}


MODULES: Hash = {}


NAMES: Hash = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
