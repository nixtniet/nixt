# This file is placed in the Public Domain.


"basic commands"


import time


from nixt.defines import Commands, Main, Mods, Time, Utils


def cmd(event):
    "list available commands."
    cmds = list(Commands.cmds.keys())
    cmds.extend(Mods.list())
    event.reply(",".join(sorted(cmds)))


Commands.add(cmd)


def mod(event):
    "list available modules."
    mods = list(Commands.names.keys())
    if not mods:
        event.reply("no modules available")
        return
    event.reply(",".join(mods))


Commands.add(mod)


def help(event):
    if not event.cmd:
        mods = ",".join(Mods.list())
        event.reply(f"hlp <{mods}>")
        return
    name = event.cmd
    mod = Mods.get(name)
    dispatcher = getattr(mod, "Cmd", False)
    if not dispatcher:
        event.reply("no commands in %s module." % name)
        return
    if not event.args:
        event.reply(f"{name} <{Utils.skip(dispatcher)}")
    else:
        funcname = event.args[0] 
        function = getattr(dispatcher, funcname, False)
        if not function:
            event.reply(f"no {funcname}  command in {name} module")
            return
        comment = getattr(function, "__doc__", False)
        if not comment:
            event.reply(f"no docstring for {funcname} command.")
        event.reply(comment)
        

Commands.add(help)
