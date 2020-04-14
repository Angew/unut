import doctest
import unittest

import statics
from statics import *


class TestWithStatics(unittest.TestCase):
    def test_simple(self):
        @with_statics
        def counter(static):
            static.x = static.current.x or 0
            static.x += 1
            return static.x
        self.assertSequenceEqual(
            (counter(), counter(), counter()),
            (1, 2, 3)
        )

    def test_unique_init_calls(self):
        @with_statics
        def counter(static, init):
            static.x = static.current.x or init()
            static.x += 1
            return static.x
        inits = []
        def init():
            inits.append(None)
            return 0
        self.assertSequenceEqual(
            (counter(init), counter(init), counter(init)),
            (1, 2, 3)
        )
        self.assertSequenceEqual(inits, [None])

    def test_unique_init_loop(self):
        @with_statics
        def counter(static, init, count):
            for i in range(count):
                static.x = static.current.x or init()
                static.x += 1
            return static.x
        inits = []
        def init():
            inits.append(None)
            return 0
        self.assertEqual(counter(init, 3), 3)
        self.assertSequenceEqual(inits, [None])

    @unittest.skipUnless(__debug__, "requires __debug__ run of Python")
    def test_name_mismatch_assertion(self):
        @with_statics
        def function(static):
            static.x = static.current.x or 0
            static.y = static.current.x or 1
            return static.y
        with self.assertRaises(AssertionError) as ex:
            function()
        msg = str(ex.exception)
        self.assertRegex(msg, r"static\.current\.x")
        self.assertRegex(msg, r"static\.x")
        self.assertRegex(msg, r"static\.y")

    def test_instance_method(self):
        class Subject:
            def __init__(self):
                self.val = 0
            @with_statics
            def act(static, self):
                static.x = static.current.x or 0
                self.val += static.x
                static.x += 1
                return self.val
        s = Subject()
        self.assertSequenceEqual(
            (s.act(), s.act(), s.act()),
            (0, 1, 3)
        )

    def test_class_method(self):
        class Subject:
            val = 0
            @classmethod
            @with_statics
            def act(static, cls):
                static.x = static.current.x or 0
                cls.val += static.x
                static.x += 1
                return cls.val
        self.assertSequenceEqual(
            (Subject.act(), Subject.act(), Subject.act()),
            (0, 1, 3)
        )


def run():
    if not doctest.testmod(statics)[0]:
        print("doctest: OK")
    unittest.main()


if __name__ == "__main__":
    run()
