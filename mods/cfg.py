# This file is placed in the Public Domain.


"configuration"


from nixt.defines import Base, Disk, Object, Mods


whitelist = ['cfg']


def cfg(event):
    "configure modules."
    if not event.args:
        mods = f"{'main,' + Mods.has('Config')}"
        if mods.endswith(","):
            mods = mods[:-1]
        event.iface(f"<{mods}>")
        return
    name = event.args[0]
    cfg = Base()
    Disk.read(cfg, name, "config")
    if name != "main" and not cfg:
        mod = Mods.get(name)
        if not mod:
            event.reply(f"no {name} module found.")
            return
        cfg = getattr(mod, "Config", None)
        if not cfg:
            event.reply(f"no {name} config found.")
            return
    if not event.sets:
        event.reply(
            Object.fmt(
                cfg,
                Object.keys(cfg),
                skip=["word",]
            )
        )
        return
    Object.edit(cfg, event.sets)
    Disk.write(cfg, name, "config")
    event.ok()
