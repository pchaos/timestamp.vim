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
logger = logging.getLogger(__name__)


class classname(unittest.TestCase):
    def setUp(self):
        self.substitute = insert_timestamp.substitute
        self.pattern = r"((Last ([cC]hanged?|modified)|Modified)\s*:\s+)\d{4}-\d{2}-\d{2}(\s*|T)?\d{2}:\d{2}:\d{2}(\s*)?|TIMESTAMP"
        logger.info(self.pattern)

    def tearDown(self):
        self.substitute = None

    def _substitue(
        self,
        pattern,
        replacestr="2022-01-01 12:01:01",
        string="Modified: 2022-07-07 19:35:31 ",
    ):
        logger.info(f"{pattern=}\n{replacestr=}\n{string=}")
        rv = self.substitute(string, pattern, replacestr)
        logger.info(f"{rv=}")
        return rv

    def test_substitute(self):
        rv = self._substitue(self.pattern)
        string = "Modified: 2022-07-07 19:35:31 "
        self.assertTrue(rv != string, "not replace:{string}, {rv}")

        pattern = "((Last ([cC]hanged?|modified)|Modified)\s*:\s+)\d{4}-\d{2}-\d{2}(\s*|T)?\d{2}:\d{2}:\d{2}(\s*)?|2022-07-08 08:37:31"
        rv2 = self._substitue(pattern)
        self.assertTrue(
            rv == rv2, 'Pattern using "r" or no "r" must be equal.{rv} != {rv2}'
        )

    def test_substitute2(self):
        pass
