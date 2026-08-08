# This file is placed in the Public Domain.


"a clean namespace"


from .objects import Default


class Parse:

    @classmethod
    def parse(cls, obj, text, clean=False):
        "parse text for command and arguments."
        data = {
            "args": [],
            "cmd": "",
            "gets": Default(),
            "index": None,
            "init": "",
            "mod": "",
            "opts": "",
            "otxt": text,
            "rest": "",
            "silent": Default(),
            "sets": Default(),
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
            obj.text = obj.mod + " " + obj.cmd
            obj.rest = " ".join(obj.args)
            obj.text = obj.text + " " + obj.rest
        else:
            obj.text = obj.mod + " " + obj.cmd

    @classmethod
    def typed(cls, obj, key, val):
        "assign proper types."
        if not val:
            return
        if val in ["True", "true", True]:
            return setattr(obj, key, True)
        if val in ["False", "false", False]:
            return setattr(obj, key, False)
        try:
            return setattr(obj, key, int(val))
        except ValueError:
            pass
        try:
            return setattr(obj, key, float(val))
        except ValueError:
            pass
        setattr(obj, key, val)


def __dir__():
    return (
        'Parse',
    )
