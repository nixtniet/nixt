# This file is placed in the Public Domain.


"configuration"


from nixt.methods import Methods
from nixt.objects import Dict
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
    config = getattr(mod, "Config", None)
    if not config:
        event.reply("no configuration found.")
        return
    fnm = Locate.first(config) or Methods.ident(config)
    if not event.sets:
        event.reply(
            Methods.fmt(
                config,
                Dict.keys(config),
                skip=["word",]
            )
        )
        return
    Methods.edit(config, event.sets)
    Disk.write(Methods.skip(config), fnm)
    event.reply("ok")
