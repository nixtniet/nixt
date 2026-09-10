# This file is placed in the Public Domain.


"tables"


CORE = {
    "booting": "33ce47d91d23e2f08ea3c88ba729c8cf",
    "brokers": "7b538e39c4cbf771cfc7aa7af9ee6b0b",
    "clients": "76dbf2500f53dd1f2d0dbc50c9edf35b",
    "command": "ffcc1f6594f913efef6628294b9de515",
    "configs": "a76957a9575874a43e19d348e61ac6f6",
    "defines": "f6da40af2240d015d28ce6224bbbe664",
    "encoder": "92d40ef5ae50cafba6cc88b0e260b012",
    "engines": "6e08062628b324ff8ead4aaacdcadb32",
    "fetcher": "350fdb8ddc37c23fbad9685bc8f5a0fe",
    "loggers": "bff3f83a7436a45814853a34ca069251",
    "looping": "6a8f6f3369dc6b4980d68087941857d2",
    "message": "a4095faea9fabfeb87f9abe05da599f1",
    "objects": "7b4de5cab301c4bb56c153a4854e09a3",
    "package": "8c57813abd9552cf860750dbaab39ad7",
    "parsers": "bbb1a0183c61bd9fea612ec00eedeb33",
    "persist": "dd76d5cc15d3c16372ea34e51fa4a1f7",
    "pooling": "a5f0bb7e5eefaa765e97ce9b0be640b1",
    "repeats": "c103268a6570558d1d53e2d2161d804c",
    "require": "bc38ac96f2f7a6d338df77c860839989",
    "runtime": "890f15911009d9f3d71b3937c66924b0",
    "threads": "bf204b132a637089383f407e58b553db",
    "utility": "7736fb6aa8e951c0630531f1aa2d596c",
    "watcher": "fd271e485857938561742702fcf12356"
}


MODULES = {
    "cfg": "83bd7e9b313fb55fc46c7bf797a70f77",
    "eml": "d1aa1a59b40a4c3d1fadcbf2424b8880",
    "fie": "bc9361e18eefa2a97be4fa806021e53b",
    "flt": "c40a68583139d18206d885959c0ece30",
    "fnd": "bf337a3d5b00f942441638e450553030",
    "hlp": "0e3fe796350fb7707e218e4a94f440b8",
    "irc": "398a8520c899ad463066d8cac84b521a",
    "log": "5d11a098f0c298fe773f8d9bfbb21d11",
    "man": "920599410f7739c9503e0eea9e4e5885",
    "mdl": "fdd0773090bb067ae0efdd611d64f0b1",
    "opm": "758a02ce54aff5a0580702865454858f",
    "pth": "1b7e056a0f4e258dde8dc80e31cbd17a",
    "req": "bc1984d2e9de0310dc1b468f25c7ab8c",
    "rss": "598faa4d6a50c0f6ea07bf96efba9af0",
    "sil": "6409941fa5f1f20a23f37774ec0c6a7d",
    "slg": "e68f11973ddc2e3edeb0de0e16e9fe7a",
    "srv": "0c6cf401023c4b0fd13a06271ae3ddcb",
    "tdo": "e472d38368e3a278581caeeff08be558",
    "thr": "a9ab22cec2f1e919e09c243af21f306c",
    "tmr": "61c1044f61d778f3ecaf33ed25202acd",
    "upt": "d7f456e017f217289720a0ddda3aa24d",
    "ver": "34380fe0a4bacc6379593e99a3633054",
    "wsd": "577b9cbf15e731bcab8458e2343125a5"
}


NAMES = {
    "atr": "rss",
    "cfg": "cfg",
    "dis": "mdl",
    "dne": "tdo",
    "dpl": "rss",
    "eml": "eml",
    "exp": "opm",
    "fie": "fie",
    "flt": "flt",
    "fnd": "fnd",
    "hlp": "hlp",
    "imp": "opm",
    "log": "log",
    "lou": "sil",
    "man": "man",
    "mbx": "eml",
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
