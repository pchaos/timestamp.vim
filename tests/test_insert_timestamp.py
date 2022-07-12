# coding=utf-8
# Modified: 2022-07-09 23:05:27

import logging
import os
import re
import sys
import unittest


def set_syspath():
    print(f"{sys.path=}")
    print(f"{os.path.join('./', '../python')=}")
    if os.path.exists("../python"):
        sys.path.insert(0, os.path.join("./", "../python"))
        print(f"insert path:{os.path.join('./', '../python')}")
    elif os.path.exists("python"):
        sys.path.insert(0, os.path.join("./", "python"))
        print(f"insert path:{os.path.join('./', 'python')}")
    print(f"{sys.path=}")


set_syspath()
import insert_timestamp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Insert_timestamp_test(unittest.TestCase):
    def setUp(self):
        self.substitute = insert_timestamp.substitute
        # self.pattern = r"((Last\s+([cC]hanged?|modified)|Modified)\s*:\s+)\d{4}-\d{2}-\d{2}(\s*|T)?\d{2}:\d{2}:\d{2}(\s*)?|TIMESTAMP"
        self.pattern = r"((Last\s+([cC]hanged?|[mM]odified)|Modified)\s*:\s+)\d{4}-\d{2}-\d{2}(\s*|T)?\d{2}:\d{2}:\d{2}(\s*)?|TIMESTAMP"
        self.string = "Modified: 2022-07-07 19:35:31 "
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
        rv = self.substitute(pattern, replacestr, string )
        logger.info(f"replaced:{rv}")
        return rv

    def _check_search(self, pattern, string):
        rs = re.search(pattern, string)
        logger.info(f"checking:{pattern=}\n{string=}")
        self.assertTrue(rs is not None, "searched:{rs}\n{re.search(pattern, string)=}")
        return rs

    def test_substitute(self):
        rv = self._substitue(self.pattern)
        string = "Modified: 2022-07-07 19:35:31 "
        self.assertTrue(rv != string, "not replace:{string}, {rv}")

        # pattern不用前缀"r"
        pattern = "((Last ([cC]hanged?|modified)|Modified)\s*:\s+)\d{4}-\d{2}-\d{2}(\s*|T)?\d{2}:\d{2}:\d{2}(\s*)?|2022-07-08 08:37:31"
        rv2 = self._substitue(pattern)
        self.assertTrue(
            rv == rv2, 'Pattern using "r" or no "r" must be equal.{rv} != {rv2}'
        )

    def test_substitute_chinese_string(self):
        chinese_str = "带中文字符"
        string = f"{chinese_str} {self.string}"
        rv = self._substitue(self.pattern, string=string)
        logger.info(f"After substitue")
        rs = re.search(chinese_str, rv)
        self.assertTrue(
            rs is not None,
            "chinese string not found in {rv}:{rs}\n{re.search(chinese_str, string)=}",
        )
        self._check_search("Modified", rv)
        rs2 = re.search(chinese_str, rv)
        self.assertTrue(rs2 is not None, "chinese string not found in {rv2}:{rs}")
        logger.info(f"chinese_str result::{string} chinese string replaced: {rv} {rs}")

    def test_substitute_repalce_twice(self):
        chinese_str = "带中文字符"
        string = f"{chinese_str} {self.string}"
        rv = self._substitue(self.pattern, string=string)
        pattern = r"\d{4}-\d{2}-\d{2}(\s*|T)?\d{2}:\d{2}:\d{2}(\s*)?"
        rv2 = self._substitue(pattern, string=rv)
        logger.info(f"return value:'{rv}'\nreturn vallue2:'{rv2}'")
        self.assertTrue(rv == rv2, "twice replace :{rv==rv2}")
        replacestr = "0000-01-01 01:01:01"
        rv3 = self._substitue(pattern, replacestr=replacestr, string=rv)
        logger.info(f"return vallue3:'{rv3}'")
        self.assertTrue(rv != rv3, "twice replace :{rv==rv3}")

    def test_substitute_2(self):
        string = "Modified:  2022-07-07 15:52:56"
        replacestr = "0000-01-01 01:01:01"
        rv = self._substitue(self.pattern, replacestr=replacestr, string=string)
        result_string = "Modified:  0000-01-01 01:01:01"
        self.assertTrue(rv == result_string,  'expected result：{rv}  != {result_string}')

    def test_substitute_3(self):
        string = "Modified:  TIMESTAMP"
        replacestr = "0000-01-01 01:01:01"
        rv = self._substitue(self.pattern, replacestr=replacestr, string=string)
        result_string = "Modified:  0000-01-01 01:01:01"
        self.assertTrue(rv == result_string,  'expected result：{rv}  != {result_string}')

    def test_substitute_4(self):
        string = "Modified:\tTIMESTAMP"
        replacestr = "0000-01-01 01:01:01"
        rv = self._substitue(self.pattern, replacestr=replacestr, string=string)
        result_string = "Modified:\t0000-01-01 01:01:01"
        self.assertTrue(rv == result_string,  'expected result：{rv}  != {result_string}')

    def test_substitute_5(self):
        string = "; Modified: 2022-07-10 11:25:24 "
        replacestr = "0000-01-01 01:01:01"
        rv = self._substitue(self.pattern, replacestr=replacestr, string=string)
        result_string = "; Modified: 0000-01-01 01:01:01"
        self.assertTrue(rv == result_string,  'expected result：{rv}  != {result_string}')

    def test_substitute_6(self):
        string = "-- Last Modified:   2022-07-07 11:32:34 "
        replacestr = "0000-01-01 01:01:01"
        rv = self._substitue(self.pattern, replacestr=replacestr, string=string)
        result_string = "-- Last Modified:   0000-01-01 01:01:01"
        self.assertTrue(rv == result_string,  'expected result：{rv}  != {result_string}')

    def test_substitute_7(self):
        string = "-- Last modified:   2022-07-07 11:32:34 "
        replacestr = "0000-01-01 01:01:01"
        rv = self._substitue(self.pattern, replacestr=replacestr, string=string)
        result_string = "-- Last modified:   0000-01-01 01:01:01"
        self.assertTrue(rv == result_string,  'expected result：{rv}  != {result_string}')

    def test_substitute_8(self):
        string = "-- Last changed:   2022-07-07 11:32:34 "
        replacestr = "0000-01-01 01:01:01"
        pattern = "abc changed"
        rv = self._substitue(pattern, replacestr=replacestr, string=string)
        result_string = "-- Last changed:   0000-01-01 01:01:01"
        self.assertTrue(rv == result_string,  'expected result：{rv}  != {result_string}')

        string = "-- Last Changed:   2022-07-07 11:32:34 "
        replacestr = "0000-01-01 01:01:01"
        rv = self._substitue(pattern, replacestr=replacestr, string=string)
        result_string = "-- Last Changed:   0000-01-01 01:01:01"
        self.assertTrue(rv == result_string,  'expected result：{rv}  != {result_string}')


        # 不包含'changed'
        pattern = "abc "
        rv = self._substitue(pattern, replacestr=replacestr, string=string)
        result_string = "-- Last changed:   0000-01-01 01:01:01"
        self.assertTrue(rv != result_string,  'expected result：{rv}  != {result_string}')


if __name__ == "__main__":
    unittest.main()
