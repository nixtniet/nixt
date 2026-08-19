# This file is placed in the Public Domain.


"tables"


CORE = {
    "booting": "4465f93752a9a1e8e31f7c9d8140bebe",
    "brokers": "bf614fd92d3268216c853bbb08a57b03",
    "clients": "9bd824df44ceeeaf73134e38f8177669",
    "command": "2e9fc0aaa8dde0d8caccea26b3feb066",
    "configs": "55373ef42c73f1df77f0a29755fe6027",
    "defines": "36401acdf41a9fde255e2b9d3afbe078",
    "encoder": "7c7f68bbcdc0bd9955c0acf70a9b4d7c",
    "engines": "767e741a9e84f56cdb1b68c979a6b584",
    "hashing": "1b7cb34eaff614661f28ad870299ba98",
    "loggers": "0c75c9b5df26dc5f023257711f140754",
    "message": "6c2322224bbca893fd5899bda65df43e",
    "methods": "dc4c2e41f7a6cf82584e8119ee6725fa",
    "objects": "529a55e137b6f5bd5908fdcdd1049d86",
    "outputs": "b7edddf1249f1be8b9e568379479948f",
    "package": "9d94c9c55f2046ac1cd00e1a6f58d5eb",
    "parsers": "cc9923d5e2e0aab885247a530ac0970c",
    "persist": "49e11f383821f99816f40c5bf2e304d6",
    "repeats": "eaec4feccb68aea97288b5729d710454",
    "require": "53ae8d308fceff8dab77fc89f86f7eef",
    "runtime": "ed941e3697f861b0cd3a175f29fcd991",
    "threads": "2fcb5ceb0fa336dd7208297fc23e17b0",
    "timings": "3779158dd2a2f280d403717c7ea75886",
    "utility": "973787cf63dccce61d10b16722c08355"
}


MODULES = {
    "cfg": "83bd7e9b313fb55fc46c7bf797a70f77",
    "fie": "0eb10b5104e76831e1295ff9a91a0e8d",
    "flt": "c40a68583139d18206d885959c0ece30",
    "fnd": "d8c272c7912b46a1ef678d63b0895d45",
    "hlp": "0e3fe796350fb7707e218e4a94f440b8",
    "irc": "c332ea54145a98f2b0983b40292a1e13",
    "log": "5d11a098f0c298fe773f8d9bfbb21d11",
    "man": "920599410f7739c9503e0eea9e4e5885",
    "mdl": "0ea87138ce166ce9a904514ab8bc4b48",
    "pth": "3a13aaa5724170f64394c52a4596d53b",
    "req": "bc1984d2e9de0310dc1b468f25c7ab8c",
    "rss": "dba26a0bc060ffb5c805e0ad286b3ebc",
    "rst": "39b1e1c5fe013f6a19aa3d378a383cf7",
    "sil": "6409941fa5f1f20a23f37774ec0c6a7d",
    "slg": "e68f11973ddc2e3edeb0de0e16e9fe7a",
    "srv": "5c383f3ac95404a837164e7ec03adac4",
    "tdo": "734baf117bde28e7a979bdec82528c14",
    "thr": "6ae37c096264d246cb4de07cfd687222",
    "tmr": "f3d6df1887dae91a3023350749f4217a",
    "udp": "abc7949f82db4990c2d569fa4325dba9",
    "upt": "d7f456e017f217289720a0ddda3aa24d",
    "ver": "be405e2a3d958c3ae704adb3d3fb3c6d",
    "web": "fedf1a525e75f1a7e16c2503a700f03a",
    "wsd": "a9d4f77c24929ec37b62044b9e83023a"
}


NAMES = {
    "atr": "rss",
    "cfg": "cfg",
    "dis": "mdl",
    "dne": "tdo",
    "dpl": "rss",
    "err": "rss",
    "exp": "rss",
    "fie": "fnd",
    "flt": "flt",
    "fnd": "fnd",
    "hlp": "hlp",
    "imp": "rss",
    "log": "log",
    "lou": "sil",
    "man": "man",
    "nme": "rss",
    "now": "mdl",
    "pth": "pth",
    "pwd": "irc",
    "rem": "rss",
    "req": "req",
    "res": "rss",
    "rss": "rss",
    "sil": "sil",
    "slg": "slg",
    "srv": "srv",
    "syn": "rss",
    "tdo": "tdo",
    "thr": "thr",
    "tmr": "tmr",
    "udp": "udp",
    "upt": "upt",
    "ver": "ver",
    "wsd": "wsd"
}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
