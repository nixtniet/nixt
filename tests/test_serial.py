# This file is placed in the Public Domain.


import unittest
import json


from io import StringIO


from nixt.serial import dump, dumps, load, loads, Encoder, hook
from nixt.object import Object


class TestEncoder(unittest.TestCase):

    def test_default_object(self):
        pass

    def test_default_dict(self):
        pass

    def test_default_list(self):
        pass

    def test_default_other_type(self):
        pass

    def test_default_unserializable(self):
        pass


class TestHook(unittest.TestCase):

    def test_hook(self):
        pass


class TestSerializationFunctions(unittest.TestCase):

    def test_dump_and_load(self):
        pass

    def test_dumps_and_loads(self):
        pass

    def test_nested_objects(self):
        pass


if __name__ == '__main__':
    unittest.main()
