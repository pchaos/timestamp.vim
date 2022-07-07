# coding=utf-8
import logging
import os
import sys
import unittest

print(f"{sys.path=}")
print(f"{os.path.join('./', '../python')=}")
if os.path.exists("../python"):
    sys.path.insert(0, os.path.join("./", "../python"))
    print(f"insert path:{os.path.join('./', '../python')}")
elif os.path.exists("python"):
    sys.path.insert(0, os.path.join("./", "python"))
    print(f"insert path:{os.path.join('./', 'python')}")
print(f"{sys.path=}")

import insert_timestamp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


class classname(unittest.TestCase):
    def setUp(self):
        self.substitute = insert_timestamp.substitute
        logger.info(self.substitute)

    def tearDown(self):
        self.substitute = None

    def test_substitute(self):
        pattern = "((Last ([cC]hanged?|modified)|Modified)\s*:\s+)\d{4}-\d{2}-\d{2}(\s*|T)?\d{2}:\d{2}:\d{2}(\s*)?|TIMESTAMP"
        string = "Modified: 2022-07-07 19:35:31 "
        replacestr = "2022-01-01 12:01:01"
        rv = self.substitute(string, pattern, replacestr)
        self.assertTrue(rv != string, "not replace:{string}, {rv}")
        logger.info(f"{rv=}")

    def test_substitute2(self):
        pass
