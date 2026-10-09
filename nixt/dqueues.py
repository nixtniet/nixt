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
        self.index: int = 0
        self.lock: RLock = RLock()
        self.ltime: float = 0.0
        self.path: str = path
        Utils.cdir(self.path)
        pathlib.Path(self.path).touch()
        Logging.enable(self.path, Log)

    def get(self) -> Union[Message, None]:
        "get message from disk."
        with self.lock, open(self.path, "a+", encoding="utf-8") as file:
            while True:
                file.seek(2)
                indx = file.tell()
                if indx <= self.index:
                    time.sleep(1.0)
                    continue
                file.seek(self.index, 0)
                line = file.readline()
                msg = Message()
                try:
                    Method.construct(msg, JSONL.loads(line.strip()))
                    return msg
                except json.decoder.JSONDecodeError as ex:
                    Log.exception(ex)
                    del msg                    
                self.index = file.tell()
        return None

    def put(self, msg: Message):
        "put message to disk."
        with open(self.path, "a+", encoding="utf-8") as file:
            JSONL.write(msg, file)

    def qsize(self):
        "return size."
        return self.index

    def task_done(self):
        "dummy"


def __dir__():
    return (
        'DQueue',
    )
