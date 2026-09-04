# This file is placed in the Public Domain.


"tables"


CORE = {
    "booting": "ac42d9c7043a1f7a331abdeac7fa87b0",
    "brokers": "12fa66535cefa5cbe072200cf590f362",
    "clients": "1fccf3868288dec52fae3cce4b1f565e",
    "command": "ee7da9fb0c7f941f061c73e2380ad77a",
    "configs": "55373ef42c73f1df77f0a29755fe6027",
    "defines": "9b3aebaa1644eaa3fdf4bece1c6ec1c5",
    "encoder": "749faec2870ee53b1bbe11a340a3f947",
    "engines": "767e741a9e84f56cdb1b68c979a6b584",
    "fetcher": "e3598be7c6372dd0114d42132d94fbd0",
    "hashing": "3e4bb889cdd9c4213271854245150442",
    "message": "6c2322224bbca893fd5899bda65df43e",
    "methods": "1b1d7d46d5f1253d905f6a13de075ce9",
    "objects": "529a55e137b6f5bd5908fdcdd1049d86",
    "outputs": "d5f2fe82a55ff7f59ff3f844aba9c8e2",
    "package": "86138f602eb904c4c9215a8454da745f",
    "parsers": "de88da518e5ca1b61346cb327eb538e2",
    "persist": "aa1c67749f328d575707af0fff57976e",
    "repeats": "eaec4feccb68aea97288b5729d710454",
    "require": "2d58f56948cce0c558d8be7a39e9b59f",
    "runtime": "a3f0ffe9b0f5ca8e13c4c6c78a1f44c0",
    "threads": "2fcb5ceb0fa336dd7208297fc23e17b0",
    "utility": "7bfc5e8741007048fac03878ee0b2181",
    "watcher": "5931b135a43dc4c5bb54cd07ba9ff713"
}


MODULES = {
    "cfg": "a47404e23ba563ebc0c3ac7a99fb8b77",
    "fnd": "c7816bb51a83be76bcccf5bc514f367b",
    "irc": "17968cb01c5f9c51c35b6ee641911a9a",
    "opm": "ad51933f934d29118e1e14ccf8e349ab",
    "rss": "da7d88c7fc4d09fc0715559020cc95cf",
    "srv": "a453db7d9e9cb6be08f33aeabba04edb",
    "thr": "aa9d092137049239127bbf5b85599018",
    "upt": "4e8110d1b93254cd6555a619b2b78ccc"
}


NAMES = {
    "atr": "rss",
    "cfg": "cfg",
    "dpl": "rss",
    "exp": "opm",
    "fnd": "fnd",
    "imp": "opm",
    "nme": "rss",
    "pwd": "irc",
    "rem": "rss",
    "res": "rss",
    "rss": "rss",
    "srv": "srv",
    "syn": "rss",
    "thr": "thr",
    "upt": "upt"
}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
