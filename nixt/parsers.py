# This file is placed in the Public Domain.


"option parsing"


from .objects import Base, Object


class Parse:

    @staticmethod
    def parse(obj, text, clean=False):
        "parse text for command and arguments."
        data = {
            "args": [],
            "cmd": "",
            "gets": Base(),
            "index": None,
            "init": "",
            "mod": "",
            "opts": "",
            "otxt": text,
            "rest": "",
            "silent": Base(),
            "sets": Base(),
            "text": text
        }
        for k, v in data.items():
            if not clean:
                setattr(obj, k, getattr(obj, k, v) or v)
            else:
                setattr(obj, k, v)
        args = []
        nr = -1
        for spli in text.split():
            if spli.startswith("-"):
                try:
                    obj.index = int(spli[1:])
                except ValueError:
                    obj.opts += spli[1:]
                continue
            if "-=" in spli:
                key, value = spli.split("-=", maxsplit=1)
                Object.typed(obj.silent, key, value)
                Object.typed(obj.gets, key, value)
                continue
            if "==" in spli:
                key, value = spli.split("==", maxsplit=1)
                Object.typed(obj.gets, key, value)
                continue
            if "=" in spli:
                key, value = spli.split("=", maxsplit=1)
                Object.typed(obj.sets, key, value)
                continue
            nr += 1
            if nr == 0:
                obj.mod = spli
                continue
            if nr == 1:
                obj.cmd = spli
                continue
            args.append(spli)
        if args:
            obj.args = args
            obj.text = obj.cmd or ""
            obj.rest = " ".join(obj.args)
            obj.text = obj.cmd + " " + obj.rest
        else:
            obj.text = obj.cmd or ""
        Object.notset(obj, obj.sets)


def __dir__():
    return (
        'Parse',
    )
