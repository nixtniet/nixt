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


def eml(message):
    "search emails."
    nrs = -1
    args = ["From", "Subject"]
    args.extend(message.args)
    if message.gets:
        args.extend(Method.keys(message.gets))
    for key in message.silent:
        if key in args:
            args.remove(key)
    arguments = list(set(args))
    result = sorted(
                    Locater.find("email", message.gets),
                    key=lambda x: Time.timed(x[1].Date)
                   )
    if message.index not in ["", None]:
        obj = result[message.index]
        if obj:
            obj = obj[-1]
            tme = getattr(obj, "Date", "")
            diff = time.time() - Time.timed(tme)
            txt = Method.fmt(obj, arguments, plain=True)
            message.reply(f'{message.index} {txt} {Time.elapsed(diff)}')
    else:
        for _fn, obj in result:
            nrs += 1
            tme = getattr(obj, "Date", "")
            diff = time.time() - Time.timed(tme)
            txt = Method.fmt(obj, arguments, plain=True)
            message.reply(f'{nrs} {txt} {Time.elapsed(diff)}')
    if not result:
        message.reply("no emails found.")


def mbx(message):
    "import emails from mailbox."
    if not message.args:
        message.iface("<path>")
        return
    fnm = os.path.expanduser(message.args[0])
    if not os.path.exists(fnm):
        message.iface("<path>")
        return
    message.reply(f"reading from {fnm}")
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
            message.ok(nrs)
    except FileNotFoundError as ex:
        message.reply(str(ex))
