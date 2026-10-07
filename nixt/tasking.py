# This file is placed in the Public Domain.


"non-blocking"


import inspect
import time
import _thread


from .default import Event, Logger, Queue, RLock, Thread
from .typings import Any, Callable, ClassVar, Dict, Union


Anys    = Dict[str, Any]
Log     = Logger(__name__)
TimeOut = Union[float, None]


class Worker(Thread):

    "unit of thread"

    block: ClassVar[Event] = Event()

    def __init__(self, func, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, None, (), daemon=daemon)
        self.name: str = kwargs.get("name", self.getname(func) or "")
        self.queue: Queue = Queue()
        self.result: Any = None
        self.sleep: float = 0.0
        self.starttime: float = time.time()
        self.state = Anys
        self.queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def join(self, timeout: TimeOut = None) -> Union[Any, None]:
        "join thread and return result."
        try:
            super().join(timeout or None)
            return self.result
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()
            return None

    def clsname(self, obj: Any) -> str:
        "class name of an object."
        if "__self__" in dir(obj):
            return obj.__self__.__class__.__name__
        return obj.__class__.__name__

    def getname(self, obj: Any) -> str:
        "string of function/method."
        if inspect.ismethod(obj):
            return f"{self.clsname(obj)}.{obj.__name__}"
        if inspect.isfunction(obj):
            return repr(obj).split()[1]
        return repr(obj)

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
            Log.exception(str(func))
            _thread.interrupt_main()


class Task:

    "start a task"

    lock: ClassVar[RLock] = RLock()

    @classmethod
    def start(cls, func: Callable, *args: Any, **kwargs: Any) -> Worker:
        "start a new thread running function with arguments."
        with cls.lock:
            worker = Worker(func, *args, **kwargs)
            worker.start()
            return worker


def __dir__():
    return (
        'Task',
        'Worker'
    )
