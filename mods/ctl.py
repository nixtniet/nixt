# This file is placed in the Public Domain.


"control"


from nixt.defines import Main, Runtime


def cmd(text):
    cli = Line()
    for txt in text.split(" ! "):
        evt = Event()
        evt.kind = "command"
        evt.orig = repr(cli)
        evt.text = txt
        Commands.command(evt)
        evt.wait()



def control():
    "cli script."
    import sys
    txt = " ".join(sys.argv[1:])
    if not txt:
        return
    Main.all = True
    Runtime.configure(Main)
    Runtime.scan(Main)
    cmd(txt)
