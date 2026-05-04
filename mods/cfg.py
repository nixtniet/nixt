# This file is placed in the Public Domain.


"configuration"


from nixt.defines import Object, Disk, Methods, Mods, Dict


def cfg(event):
    "configure."
    if not event.args:
        mods = f"{'main,' + Mods.has('Config')}"
        if mods.endswith(","):
            mods = mods[:-1]
        event.reply(f"cfg <{mods}>")
        return
    name = event.args[0]
    config = Object()
    Disk.read(config, name, "config")
    if name != "main" and not config:
        mod = Mods.get(name)
        if not mod:
            event.reply(f"no {name} module found.")
            return
        config = getattr(mod, "Config", None)
        if not config:
            event.reply("no configuration found.")
            return
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
    Disk.write(config, name, "config")
    event.ok()
