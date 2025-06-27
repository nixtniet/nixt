# This file is placed in the Public Domain.


import unittest


from nixt.fleet import Fleet


class TestFleet(unittest.TestCase):

    def setUp(self):
        Fleet.clients = {}

    def tearDown(self):
        Fleet.clients = {}

    def test_add_and_get(self):
        pass

    def test_all(self):
        pass

    def test_announce(self):
        pass

    def test_dispatch(self):
        pass

    def test_display(self):
        pass

    def test_first(self):
        pass

    def test_say(self):
        pass

    def test_shutdown(self):
        pass

    def test_wait(self):
        pass


if __name__ == '__main__':
    unittest.main()
