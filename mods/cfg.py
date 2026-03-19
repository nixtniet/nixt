# This file is placed in the Public Domain.


"configuration"


from nixt.objects import Dict, Methods
from nixt.package import Mods
from nixt.persist import Disk, Locate


def cfg(event):
    if not event.args:
        event.reply(f"cfg <{Mods.has('Config') or 'modulename'}>")
        return
    name = event.args[0]
    mod = Mods.get(name)
    if not mod:
        event.reply(f"no {name} module found.")
        return
    cfg = getattr(mod, "Config", None)
    if not cfg:
        event.reply("no configuration found.")
        return
    fnm = Locate.first(cfg) or Methods.ident(cfg)
    if not event.sets:
        event.reply(
            Methods.fmt(
                cfg,
                Dict.keys(cfg),
                skip=["word",]
            )
        )
        return
    Methods.edit(cfg, event.sets)
    Disk.write(Methods.skip(cfg), fnm)
    event.reply("ok")
