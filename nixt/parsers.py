# This file is placed in the Public Domain.


"option parsing"


from nixt.defines import Base, Object


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
                try:
                    obj.mod, obj.cmd = spli.split(".")
                except ValueError:
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
        Object.notset(obj, obj.sets)


def __dir__():
    return (
        'Parse',
    )
