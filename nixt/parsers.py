# This file is placed in the Public Domain.


"cli parser"


from .methods import Method
from .objects import Data


from typing import ClassVar


class Options:

    options: ClassVar[dict[str,str]] = {
        "help": "show this help message and exit",
        "console": "start a console.",
        "daemon": "run as background daemon.",
        "service": "run as service.",
        "all": "load all modules.",
        "verbose": "enable verbose.",
        "wait" : "wait for services to start.",
        "level": "level  set loglevel.",
    }

    values: ClassVar[dict[str,str]]  = {
        "mods": "modules to load.",
        "path": "path to modules directory.",
        "admin": "enable admin mode.",
        "scanner": "do full modules scan on boot.",
        "wdr": "set modules directory."
    }


class Parser:

    "parsing for commands"

    @classmethod
    def init(cls, obj, text, clean):
        data = {
            "args": [],
            "cmd": "",
            "gets": Data(),
            "index": None,
            "init": "",
            "mod": "",
            "opts": "",
            "otxt": text,
            "rest": "",
            "silent": Data(),
            "sets": Data(),
            "text": text
        }
        for k, v in data.items():
            if not clean:
                setattr(obj, k, getattr(obj, k, v) or v)
            else:
                setattr(obj, k, v)

    @classmethod
    def parse(cls, obj, text, clean=False):
        "parse text for command and arguments."
        cls.init(obj, text, clean)
        args = []
        nr = -1
        for spli in text.split():
            if spli.startswith("--"):
                obj.opts += f",{spli[2:]}"
                continue
            if spli.startswith("-"):
                try:
                    obj.index = int(spli[1:])
                except ValueError:
                    obj.opts += spli[1:]
                continue
            if "-=" in spli:
                key, value = spli.split("-=", maxsplit=1)
                Method.typed(obj.silent, key, value)
                Method.typed(obj.gets, key, value)
                continue
            if "==" in spli:
                key, value = spli.split("==", maxsplit=1)
                Method.typed(obj.gets, key, value)
                continue
            if "=" in spli:
                key, value = spli.split("=", maxsplit=1)
                Method.typed(obj.sets, key, value)
                continue
            nr += 1
            if nr == 0:
                obj.cmd = spli
                continue
            args.append(spli)
        if args:
            obj.args = args
            obj.text = obj.mod + " " + obj.cmd
            obj.rest = " ".join(obj.args)
            obj.text = obj.text + " " + obj.rest
        else:
            obj.text = obj.mod + " " + obj.cmd


def __dir__():
    return (
        'Parser',
    )
