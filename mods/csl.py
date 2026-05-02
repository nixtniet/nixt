# This file is placed in the Public Domain.


"console"


from nixt.defines import Event, Main, Runtime


class Line(Console):

    def raw(self, text):
        "write to console."
        print(text.encode('utf-8', 'replace').decode("utf-8"))


class CSL(Line):

    def poll(self):
        "poll for an event."
        evt = Event()
        evt.orig = repr(self)
        evt.text = input("> ")
        evt.kind = "command"
        return evt


def csl(event):
    "console script."
    import readline
    readline.redisplay()
    Runtime.configure(Main)
    if Main.verbose:
        Runtime.banner()
    Runtime.scan(Main)
    Runtime.init(Main)
    csl = CSL()
    csl.start()
    Runtime.forever()
