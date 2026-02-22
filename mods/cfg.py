# This file is placed in the Public Domain.


"configuration"


from nixt.objects import Dict, Methods
from nixt.package import Mods
from nixt.persist import Disk, Locate


def cfg(event):
    cfg = None
    mod = None
    name = ""
    if event.args:
        name = event.args[0]
    if not name:
        event.reply(f"cfg <{Mods.has('Cfg') or 'modulename'}>")
        return
    if not cfg:
        modlist = list(Mods.get(name))
        if modlist:
            mod = modlist[-1]
            cfg = getattr(mod, "Cfg", None) 
        if not cfg:
            event.reply(f"{name} has no configuration.")
            return
    if not event.sets:
        event.reply(
            Methods.fmt(
                cfg,
                Dict.keys(cfg),
                skip=["password",]
            )
        )
        return
    fnm = Locate.first(cfg) 
    Methods.edit(cfg, event.sets)
    Disk.write(cfg, fnm)
    event.reply("ok")
