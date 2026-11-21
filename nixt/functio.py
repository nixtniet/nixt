# This file is placed in the Public Domain.


"a function with an object/dict as the first argument"


import types


from .utility import Utils


class Dicts:

    "yeah"

    @classmethod
    def deleted(cls, dct):
        "check whether obj had deleted flag set."
        return "__deleted__" in dct and dct["__deleted__"]

    @classmethod
    def edit(cls, dct, setter=None, skip=False):
        "update object with dict."
        if setter is None:
            setter = {}
        for key, val in setter.items():
            if skip and val == "":
                continue
            cls.typed(dct, key, val)

    @classmethod
    def fmt(cls, dct, args=None, skip= None, plain=False, empty=False):
        "format object info printable string."
        if args is None:
            args = list(dct.keys())
        if args == []:
            args = [x for x in dct if not x.startswith("_")]
        if skip is None:
            skip = []
        txt = ""
        for key in args:
            if key.startswith("__"):
                continue
            if key in skip:
                continue
            value = dct.get(key, None)
            if value is None:
                continue
            if not empty and value == "":
                continue
            if plain:
                txt += f"{value} "
            elif isinstance(value, (int, float, dict, bool, list)):
                txt += f"{key}={value} "
            elif isinstance(value, str):
                txt += f'{key}="{value}" '
            else:
                txt += f"{key}={Utils.clsname(value)}({value!s}) "
        if txt == "":
            txt = "{}"
        return txt.strip()

    @classmethod
    def isempty(cls, dct):
        "check if all keys heve empty value."
        return all(not dct.get(key) for key in dct)

    @classmethod
    def exists(cls, dct, key):
        "return default if key doesn't exists"
        return dct.get(key, False)

    @classmethod
    def notset(cls, dct1, dct2):
        "only set if not set."
        for key, value in dct2.items():
            if dct1.get(key, False):
                continue
            if value:
                dct1[key] = value

    @classmethod
    def search(cls, dct, selector=None, matching=False):
        "check whether object matches search criteria."
        if selector is None:
            return False
        res = False
        for key, value in selector.items():
            val = dct.get(key, None)
            if not val:
                res = False
                break
            if matching and value != val:
                res = False
                break
            if str(value).lower() not in str(val).lower():
                res = False
                break
            res = True
        return res

    @classmethod
    def skip(cls, dct, char=None):
        "skip class keys containing chars."
        if char is None:
            char = "_"
        res = {}
        for key in dct:
            if char in key:
                continue
            value = dct.get(key, None)
            if not value:
                continue
            if isinstance(value, types.MethodType):
                continue
            res[key] = value
        return res

    @classmethod
    def typed(cls, dct, key, val):
        "assign proper types."
        if dct is None or not val:
            return
        if val in ["True", "true", True]:
            dct[key] = True
            return
        if val in ["False", "false", False]:
            dct[key] = False
            return
        try:
            dct[key] = int(val)
            return
        except ValueError:
            pass
        try:
            dct[key] = float(val)
            return
        except ValueError:
            pass
        dct[key] = val


def __dir__():
    return (
        'Dicts',
    )
