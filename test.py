from testclient import sadd, sismember
import unittest

class RedisTest(unittest.TestCase):
    def test_assignment(self):
        sadd("KEY","VALUE")
        self.assertIs(sismember("KEY","VALUE"),1)

    def test_sadd(self):
        self.assertIsInstance(sadd("KEY","VALUE"),int)

    def test_sismember(self):
        self.assertIsInstance(sadd("KEY","VALUE"),int)

if __name__ == '__main__':
    unittest.main()
