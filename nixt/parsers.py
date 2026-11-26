# This file is placed in the Public Domain.


"parse text for command and arguments"


from .objects import Methods


class Parser:

    "parsing for commands"

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
        if text is None:
            text = obj.text
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
                Methods.typed(obj.silent, key, value)
                Methods.typed(obj.gets, key, value)
                continue
            if "==" in spli:
                key, value = spli.split("==", maxsplit=1)
                Methods.typed(obj.gets, key, value)
                continue
            if "=" in spli:
                key, value = spli.split("=", maxsplit=1)
                Methods.typed(obj.sets, key, value)
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


def __dir__():
    return (
        'Parser',
    )
