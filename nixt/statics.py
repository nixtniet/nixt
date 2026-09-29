# This file is placed in the Public Domain.


"tables"


from .typings import Hash


CORE: Hash = {
    "booting": "032ce55a875bf6526bba9f613bd40c3c",
    "brokers": "22ffcce7ea3a3bc6744793c8875a9c5d",
    "buffers": "20e3a0813ebc95cffdb7cea70d5a9311",
    "clients": "de54fdc0d1d46e36adaca48df6381078",
    "command": "c4cf62d926374b4e095d9e248d177c31",
    "configs": "9545a7bd63d262e62f85cbb07a4a86dc",
    "defines": "3327ce15cd094bc0ca209e4469c91b3a",
    "display": "fbd0dcc5d4a7daba9ab58540dfafd14e",
    "encoder": "869c8951a8c51694901ec656be197bf5",
    "engines": "d876b24a4572f94acb59d6813f0800e2",
    "fetcher": "f13840e135a40cb4cedc3126fb3a5630",
    "loggers": "a247909a266b7fe54f1092704f1a267b",
    "looping": "63a5dcfb9397ed3dcb027aebb877837f",
    "message": "0db8f98189723f4be87f9d8cff1c4a48",
    "methods": "ac3ce5f739b251ade56d117f2eeb2912",
    "objects": "e7d8664b921306546ac5df9bf30c9b65",
    "package": "ff991fb5249a49f9fc54b4eee653bbec",
    "parsers": "53e6f850e9ab3796016ae42d39483c4e",
    "persist": "7c7c38fad177d005b8655b5e9135260f",
    "pooling": "4ca9406fdf4639a34caba67688a6eba4",
    "repeats": "bd7cd38c0d219e848daeff96e8549b3a",
    "require": "533c66880874fef8bf07e1b1305f4454",
    "runners": "33db993b1f1caa067aae298e672d6cfa",
    "runtime": "96bf1410e22eccc4cd3cddb624393aba",
    "sources": "930fb3fe293b956c47ea91d4a9ecab4a",
    "threads": "36bbb8819516282c8b0a79a802686784",
    "typings": "53c9c830d7aadd0bea63387205bb6e4c",
    "utility": "76df8c6b89d7e004dfb0d1114dd8f9cb",
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
