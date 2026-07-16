# This file is placed in the Public Domain.


"module management"


import inspect
import logging
import os


from .objects import Default, Json, Method
from .persist import Workdir
from .utility import Logging, Md5, Utils


class Commands:

    cmds = {}

    @classmethod
    def add(cls, *funcs):
        "register a command."
        for func in funcs:
            cls.cmds[func.__name__] = func

    @classmethod
    def command(cls, evt):
        "command callback."
        Parse.parse(evt, evt.text)
        func = cls.cmds.get(evt.cmd, None)
        if func:
            func(evt)
        evt.ready()

    @classmethod
    def scan(cls, mod):
        "scan module for commands."
        for nme, func in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in inspect.signature(func).parameters:
                cls.add(func)


class Mods:

    core = {}
    dirs = {}
    md5s = {}
    modules = {}

    @classmethod
    def configure(cls, name, level="warn"):
        "configure program."
        Workdir.wdr = Workdir.wdr or Workdir.home(name)
        Workdir.skel()
        cls.dir("modules", Workdir.moddir())
        Logging.size(len(name))
        Logging.level(level)
        cls.sums()
        Md5.check(cls.core)

    @classmethod
    def dir(cls, pkgname, path):
        "add module/patgh."
        cls.dirs[pkgname] = path

    @classmethod
    def get(cls, name):
        "return module from cache or import module."
        for pkgname, path in cls.dirs.items():
            modname = f"{pkgname}.{name}"
            mod = cls.modules.get(modname, None)
            if mod:
                return mod
            fnm = os.path.join(path, name + ".py")
            if not os.path.exists(fnm):
                continue
            if cls.md5s:
                md5 = Md5.md5(fnm)
                md5s = cls.md5s.get(name)
                if md5s and md5 != md5s:
                    logging.warn("mismatch %s", modname)
            return cls.importer(modname, fnm)

    @classmethod
    def has(cls, attr):
        "return list of modules containing an attribute."
        result = []
        for modname in cls.list():
            mod = cls.get(modname)
            if not getattr(mod, attr, False):
                continue
            result.append(mod.__name__.split(".")[-1])
        return ",".join(result)

    @classmethod
    def importer(cls, name, pth=""):
        "import module by path."
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, pth)
        cls.modules[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.modules[name])
        return cls.modules[name]

    @classmethod
    def list(cls, ignore=""):
        "comma seperated list of available modules."
        mods = []
        for pkgname, path in cls.dirs.items():
            if not os.path.exists(path):
                continue
            mods.extend(Utils.listdir(path, ignore))
        return sorted(set(mods))

    @classmethod
    def scanner(cls):
        "scan all modules."
        for name in cls.list():
            Commands.scan(cls.get(name))

    @classmethod
    def sums(cls):
        "read table,"
        try:
            from .statics import CORE
            cls.core.update(CORE)
        except (ImportError, SyntaxError, ValueError):
            pass
        try:
            from .statics import MODULES
            cls.md5s.update(MODULES)
        except (ImportError, SyntaxError, ValueError):
            pass


class Parse:

    @staticmethod
    def parse(obj, text, clean=False):
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


class Cmd:

    @classmethod
    def cmd(cls, event):
        "list available commands."
        event.reply(",".join(sorted(Commands.cmds)))

    def tbl(event):
        "create table."
        core = {}
        md5s = {}
        for name in Mods.list():
            module = Mods.get(name)
            md5s[name] = Md5.md5(module.__file__)
        corepath = os.path.dirname(inspect.getsourcefile(Mods))
        for path in os.listdir(corepath):
            if path.startswith("__") or not path.endswith(".py") or "statics" in path:
                continue
            name = path[:-3]
            core[name] = Md5.md5(os.path.join(corepath, path))
        event.reply("# This file is placed in the Public Domain.")
        event.reply("\n")
        event.reply('"static tables"')
        event.reply("\n")
        event.reply(f"CORE = {Json.dumps(core, indent=4, sort_keys=True)}")
        event.reply("\n")
        event.reply(f"MODULES = {Json.dumps(md5s, indent=4, sort_keys=True)}")
        


def __dir__():
    return (
        "Cmd",
        "Commands",
        'Mods',
        'Parse'
    )

