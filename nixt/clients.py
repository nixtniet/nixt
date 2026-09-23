# This file is placed in the Public Domain.


"an object for a string"


import logging
import time


from .brokers import Broker
from .message import Message


logger = logging.getLogger(__name__)


class Clients:

    "collection of clients"

    @staticmethod
    def announce(text: str) -> None:
        "announce text on all clients."
        for obj in Broker.objs("announce"):
            obj.announce(text)

    @staticmethod
    def display(event: Message) -> None:
        "display results."
        bot = Broker.get(event.orig)
        if bot:
            bot.display(event)

    @staticmethod
    def shutdown() -> None:
        "call stop on clients."
        for client in Broker.objs("wait"):
            logger.debug("wait %s", client)
            try:
                client.wait()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        for client in Broker.objs("stop"):
            logger.debug("stop %s", client)
            try:
                client.stop()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)


def __dir__():
    return (
        'Clients',
    )
