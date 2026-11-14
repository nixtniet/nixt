# This file is placed in the Public Domain.


"program your own commands"


from .methods import Methods


class Parser:

    "parsing for commands"

    typed = Methods.typed

    @classmethod
    def init(cls, obj, text, clean=False):
        "set default values."
        data = {
            "args": [],
            "cmd": "",
            "gets": {},
            "index": None,
            "init": "",
            "mod": "",
            "opts": "",
            "otxt": text,
            "rest": "",
            "silent": {},
            "sets": {},
            "text": text
        }
        for k, v in data.items():
            if not clean:
                setattr(obj, k, data.get(k, v) or v)
            else:
                setattr(obj, k, v)

    @classmethod
    def parse(cls, obj, text=None, clean=False):
        "parse text for command and arguments."
        text = text or getattr(obj, "text", None)
        if text is None:
            return
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
                cls.typed(obj.silent, key, value)
                cls.typed(obj.gets, key, value)
                continue
            if "==" in spli:
                key, value = spli.split("==", maxsplit=1)
                cls.typed(obj.gets, key, value)
                continue
            if "=" in spli:
                key, value = spli.split("=", maxsplit=1)
                cls.typed(obj.sets, key, value)
                continue
            nr += 1
            if nr == 0:
                obj.cmd = spli
                continue
            args.append(spli)
        if args:
            obj.args = args
            obj.rest = " ".join(obj.args)
            obj.text = obj.cmd + " " + obj.rest
        if "v" in obj.opts:
            obj.verbose = True
        if "t" in obj.opts:
            obj.threaded = True


def parse(event):

    def doparse(event):
        Parse.parse(event, event.txt)

    return doparse


def __dir__():
    return (
        'Parser',
    )
