# This file is placed in the Public Domain.


"show fields on an object"


from nixt.defines import Locate, Workdir


def fie(event):
    "show fields of a type."
    if not event.rest:
        res = sorted({x.split('.')[-1].lower() for x in Workdir.kinds()})
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no types")
        return
    itms = Locate.attrs(event.args[0])
    if not itms:
        event.reply("no attributes")
    else:
        event.reply(",".join(itms))
