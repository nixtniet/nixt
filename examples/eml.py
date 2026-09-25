# This file is placed in the Public Domain.


"mailbox"


import os
import time


from mailbox import Maildir, Mailbox, mbox
from typing  import Union


from nixt.defines import Data, Disk, Locater, Method, Time


Thing = Union[Mailbox, Maildir]


class Email(Data):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text: str


def eml(event):
    "search emails."
    nrs = -1
    args = ["From", "Subject"]
    args.extend(event.args)
    if event.gets:
        args.extend(Method.keys(event.gets))
    for key in event.silent:
        if key in args:
            args.remove(key)
    arguments = list(set(args))
    result = sorted(
                    Locater.find("email", event.gets),
                    key=lambda x: Time.timed(x[1].Date)
                   )
    if event.index not in ["", None]:
        obj = result[event.index]
        if obj:
            obj = obj[-1]
            tme = getattr(obj, "Date", "")
            diff = time.time() - Time.timed(tme)
            txt = Method.fmt(obj, arguments, plain=True)
            event.reply(f'{event.index} {txt} {Time.elapsed(diff)}')
    else:
        for _fn, obj in result:
            nrs += 1
            tme = getattr(obj, "Date", "")
            diff = time.time() - Time.timed(tme)
            txt = Method.fmt(obj, arguments, plain=True)
            event.reply(f'{nrs} {txt} {Time.elapsed(diff)}')
    if not result:
        event.reply("no emails found.")


def mbx(event):
    "import emails from mailbox."
    if not event.args:
        event.iface("<path>")
        return
    fnm = os.path.expanduser(event.args[0])
    if not os.path.exists(fnm):
        event.iface("<path>")
        return
    event.reply(f"reading from {fnm}")
    thing: Union[Mailbox, Maildir]
    if os.path.isdir(fnm):
        thing = Maildir(fnm, create=False)
    elif os.path.isfile(fnm):
        thing = mbox(fnm, create=False)
    else:
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    nrs = 0
    try:
        for mail in thing:
            tmp = Data()
            Method.update(tmp, mail)
            obj = Email()
            Method.update(obj, tmp._headers)
            for payload in mail.walk():
                if payload.get_content_type() == 'text/plain':
                    load =  payload.get_payload()
                    if isinstance(load, str):
                        obj.text += load
                    else:
                        for line in load:
                            obj.text += str(line)
            obj.text = obj.text.replace("\\n", "\n")
            Disk.write(obj)
            nrs += 1
        if nrs:
            event.ok(nrs)
    except FileNotFoundError as ex:
        event.reply(str(ex))
