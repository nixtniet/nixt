# This file is placed in the Public Domain.


"non-blocking"


import inspect
import logging
import queue
import threading
import time
import _thread


from queue     import Queue
from threading import Event, RLock
from typing    import Any, Callable, ClassVar, Dict, Union


logger = logging.getLogger(__name__)


class Thr(threading.Thread):

    "unit of thread"

    block: ClassVar[Event] = Event()

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.name: str = kwargs.get("name", Thread.name(func) or "")
        self.queue: Queue = Queue()
        self.result: Any = None
        self.sleep: float = 0.0
        self.starttime: float = time.time()
        self.state = Dict[str, Any]
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout: Union[float, None] = None) -> Union[Any, None]:
        "join thread and return result."
        try:
            super().join(timeout or None)
            return self.result
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
            return None

    def run(self) -> None:
        "run function."
        func, args = self.queue.get()
        if self.block.is_set():
            return
        try:
            self.result = func(*args)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
        except Exception:
            logger.exception(str(func))
            _thread.interrupt_main()


class Thread:

    "thread helper class"

    lock: RLock = RLock()

    @classmethod
    def launch(cls, func: Callable, *args: Any, **kwargs: Any) -> Thr:
        "start a new thread running function with arguments."
        with cls.lock:
            thr = Thr(func, *args, **kwargs)
            thr.start()
            return thr

    @classmethod
    def clsname(cls, obj: Any) -> str:
        "class name of an object."
        if "__self__" in dir(obj):
            return obj.__self__.__class__.__name__
        return obj.__class__.__name_

    @classmethod
    def name(cls, obj: Any) -> str:
        "string of function/method."
        if inspect.ismethod(obj):
            return f"{cls.clsname(obj)}.{obj.__name__}"
        if inspect.isfunction(obj):
            return repr(obj).split()[1]
        return repr(obj)


def __dir__():
    return (
        'Thr',
        'Thread'
    )
