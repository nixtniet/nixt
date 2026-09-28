# This file is placed in the Public Domain.


"show fields on an object"


from nixt.defines import Locater, Workdir


def fie(message):
    "show fields of a type."
    if not message.rest:
        res = sorted({x.split('.')[-1].lower() for x in Workdir.kinds()})
        if res:
            message.reply(",".join(res))
        else:
            message.reply("no types")
        return
    itms = Locater.attrs(message.args[0])
    if not itms:
        message.reply("no attributes")
    else:
        message.reply(",".join(itms))
