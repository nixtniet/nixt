# This file is placed in the Public Domain.


"persisted queue"


import select
import json
import os
import pathlib
import time


from .default import Queue, RLock, getLogger
from .encoder import JSONL
from .loggers import Logging
from .message import Message
from .methods import Method
from .typings import List, TextIO, Union
from .utility import Utils
from .watcher import Watcher


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
        self.queue: Queue = Queue()
        self.configure()

    def callback(self):
        "read from file"
        self.file.seek(self.index, 0)
        while True:
            line = cls.file.readline()
            if not line:
                break
            self.index = self.file.tell()
            msg = Message()
            try:
                data = JSONL.loads(line.strip())
                Method.construct(msg, data)
                self.queue.put(msg)
            except json.decoder.JSONDecodeError as ex:
                Log.exception(ex)
                del msg

    def configure(self):
        Utils.cdir(self.path)
        pathlib.Path(self.path).touch()
        # Logging.enable(self.path, Log)
        Watcher.add(self.path, self.callback)

    def get(self) -> Union[Message, None]:
        "get message from disk."
        return self.queue.get()

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
