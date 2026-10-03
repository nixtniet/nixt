# This file is placed in the Public Domain.


"an object for a string"


import logging


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
    def display(msg: Message) -> None:
        "display results."
        bot = Broker.get(msg.orig)
        if bot:
            bot.display(msg)


def __dir__():
    return (
        'Clients',
    )
