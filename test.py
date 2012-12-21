from redis_client import sadd, sismember
import unittest

class RedisTest(unittest.TestCase):
    def test_assignment(self):
        sadd("KEY","VALUE")
        self.assertIs(sismember("KEY","VALUE"),1)

if __name__ == '__main__':
    unittest.main()
