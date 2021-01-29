import urllib
import urllib.request

from unittest import TestCase
from python_sandbox import (
    restrict_open,
    restrict_print,
    restrict_socket_create_connection,
    InvalidOperation,
)

class Tests(TestCase):
    def test_raises_on_open(self):
        with restrict_open():
            with self.assertRaises(InvalidOperation):
                open("tests/files/test_raises_on_open.txt")

    def test_raises_on_print(self):
        with restrict_print():
            with self.assertRaises(InvalidOperation):
                print("Hello World!")

    def test_raises_trying_to_open_webpage(self):
        with restrict_socket_create_connection():
            with self.assertRaises(InvalidOperation):
                urllib.request.urlopen("https://www.duckduckgo.com")


    def test_doesnt_raise_outside_context_manager(self):
        with restrict_open():
            pass

        with open("tests/files/test_raises_on_open.txt") as f:
            pass

        with restrict_print():
            pass

        print("")
