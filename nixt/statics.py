# This file is placed in the Public Domain.


"tables"


from typing import Dict


CORE: Dict[str, str] = {
    "booting": "9497d0902c5ae6889e4d69a4c65797b8",
    "brokers": "5c4dd22dc5823ef76cffbd254cb9907f",
    "buffers": "e951cec89e18d7ed03f68406aacd6faa",
    "clients": "0b7a52d0c0faf4299a4b02d877399166",
    "command": "990667772c4c1a907a2017aa1add1e84",
    "configs": "b7c9788d6ad2c2fc3b95f51ad4e12b86",
    "defines": "66421075f718dd5bdd0dc5f2cdcf13c1",
    "display": "637cb05fc480f4220f333c1c37ee1409",
    "encoder": "037a0b7b3879252d462fa7da69c08d80",
    "engines": "3aaa547a7244a023d310df0d3cfebe0e",
    "fetcher": "72467f06f4da41c2d179cd7243fb770a",
    "loggers": "50b5f723e94a36a2543717a4edec1995",
    "looping": "6780aa8f25c8552a8c9e98714ea551b0",
    "message": "aa36aa728352561439374faa5e73f8a0",
    "methods": "9e8f4c79a597bc0ac1a8dca20c3118b7",
    "objects": "3f68d9bd68dcd88d8a187d1a80d673fe",
    "package": "3fd7da32b72669d2ea07498fda6a2ba1",
    "parsers": "9b6b0be79a35bbe328b948f5c1f0285f",
    "persist": "04810ed0a700282f684c38036ae216ea",
    "pooling": "e0c481684a5192437164fa34b39e2f46",
    "repeats": "0a23dc0e8a481a5115a6f7ad2fd4ad2b",
    "require": "a2878a1f9440c895d4e097d5a5152054",
    "runners": "5ab77a61ce8203336a7b450280644150",
    "runtime": "fadfbbdb921ca242c93a94053289c14a",
    "sources": "b40eb681481e74004fb28da699df5f9c",
    "threads": "2f3f00ea8c818b2e6d333aeb065b8956",
    "timings": "f144669d18bbd050d0ed530de39cc4c2",
    "utility": "fb351d9c66b1d7d87829a2fab6a85f51",
    "watcher": "2de982e7581900a7e31cc971c86715fa"
}


MODULES: Dict[str,str] = {}


NAMES: Dict[str, str] = {}


def __dir__():
    return (
        'CORE',
        'MODULES',
        'NAMES'
    )
