# This file is placed in the Public Domain.


"mailbox"


import os
import time


from mailbox import Maildir, mbox


from nixt.defines import Data, Dicts, Disk, Locater, Methods, Time


class Email(Data):

    "email record"


class Parser:

    "parsing for commands"

    @classmethod
    def init(cls, obj, text, clean=False):
        "set default values."
        data = {
            "args": [],
            "cmd": "",
            "gets": {},
            "index": None,
            "init": "",
            "mod": "",
            "opts": "",
            "otxt": text,
            "rest": "",
            "silent": {},
            "sets": {},
            "text": text
        }
        for k, v in data.items():
            if not clean:
                setattr(obj, k, data.get(k, v) or v)
            else:
                setattr(obj, k, v)

    @classmethod
    def parse(cls, obj, text=None, clean=False):
        "parse text for command and arguments."
        if text is None:
            text = obj.text
        cls.init(obj, text, clean)
        args = []
        nr = -1
        for spli in text.split():
            if spli.startswith("--"):
                obj.opts += f",{spli[2:]}"
                continue
            if spli.startswith("-"):
                try:
                    obj.index = int(spli[1:])
                except ValueError:
                    obj.opts += spli[1:]
                continue
            if "-=" in spli:
                key, value = spli.split("-=", maxsplit=1)
                Methods.typed(obj.silent, key, value)
                Methods.typed(obj.gets, key, value)
                continue
            if "==" in spli:
                key, value = spli.split("==", maxsplit=1)
                Methods.typed(obj.gets, key, value)
                continue
            if "=" in spli:
                key, value = spli.split("=", maxsplit=1)
                Methods.typed(obj.sets, key, value)
                continue
            nr += 1
            if nr == 0:
                obj.cmd = spli
                continue
            args.append(spli)
        if args:
            obj.args = args
            obj.rest = " ".join(obj.args)
            obj.text = obj.cmd + " " + obj.rest
        if "v" in obj.opts:
            obj.verbose = True
        if "t" in obj.opts:
            obj.threaded = True


def eml(msg):
    "search emails."
    Parser.parse(msg)
    nrs = -1
    args = ["From", "Subject"]
    args.extend(msg.args)
    if msg.gets:
        args.extend(msg.gets.keys())
    for key in msg.silent:
        if key in args:
            args.remove(key)
    arguments = list(set(args))
    result = sorted(
                    Locater.objects("email", msg.gets),
                    key=lambda x: Time.timed(x[1].Date)
                   )
    if msg.index not in ["", None]:
        try:
            dct = result[msg.index]
        except IndexError:
            msg.reply(f"{msg.index} is too high.")
            return
        if dct:
            tme = dct.get("Date", "")
            diff = time.time() - Time.timed(tme)
            txt = Dicts.fmt(dct, arguments, plain=True)
            msg.reply(f'{msg.index} {txt} {Time.elapsed(diff)}')
    else:
        for dct in result:
            nrs += 1
            tme = dct.get("Date", "")
            diff = time.time() - Time.timed(tme)
            txt = Dicts.fmt(dct, arguments, plain=True)
            msg.reply(f'{nrs} {txt} {Time.elapsed(diff)}')
    if not result:
        msg.reply("no emails found.")


def mbx(msg):
    "import emails from mailbox."
    if not msg.args:
        msg.iface("<path>")
        return
    fnm = os.path.expanduser(msg.args[0])
    if not os.path.exists(fnm):
        msg.iface("<path>")
        return
    msg.reply(f"reading from {fnm}")
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
            dct = {}
            dct.update(mail)
            dct.update(mail.get("_headers", {}))
            for payload in mail.walk():
                if payload.get_content_type() == 'text/plain':
                    load =  payload.get_payload()
                    if isinstance(load, str):
                        dct["text"] += load
                    else:
                        for line in load:
                            dct["text"] += str(line)
            dct["text"] = dct["text"].replace("\\n", "\n")
            Disk.write(dct, Disk.ident(Email))
            nrs += 1
        if nrs:
            msg.ok(nrs)
    except FileNotFoundError as ex:
        msg.reply(str(ex))
