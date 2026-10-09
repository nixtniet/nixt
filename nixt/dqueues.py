# This file is placed in the Public Domain.


"persisted queue"


import select
import json
import os
import pathlib
import time


from .default import RLock, getLogger
from .encoder import JSONL
from .loggers import Logging
from .message import Message
from .methods import Method
from .typings import List, TextIO, Union
from .utility import Utils


IO = Union[TextIO, None]
Log = getLogger(__name__)


class DQueue:

    "Disk Queue"

    def __init__(self, path):
        self.buffer: List[Message] = []
        self.file = open(path, "a+", encoding="utf-8")
        self.index: int = 0
        self.last: int = 0
        self.lock: RLock = RLock()
        self.ltime: float = 0.0
        self.path: str = path
        self.configure()

    def configure(self):
        Utils.cdir(self.path)
        pathlib.Path(self.path).touch()
        Logging.enable(self.path, Log)

    def get(self) -> Union[Message, None]:
        "get message from disk."
        self.file.seek(self.index, 0)
        while True:
            line = self.file.readline()
            if not line:
                time.sleep(0.1)
                continue
            self.index = self.file.tell()
            msg = Message()
            try:
                data = JSONL.loads(line.strip())
                Method.construct(msg, data)
                return msg
            except json.decoder.JSONDecodeError as ex:
                Log.exception(ex)
                del msg

    def put(self, msg: Message):
        "put message to disk."
        JSONL.write(msg, self.file)
        self.last = self.file.tell()

    def qsize(self):
        "return size."
        return self.index

    def task_done(self):
        "dummy"


def __dir__():
    return (
        'DQueue',
    )
