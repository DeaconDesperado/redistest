from redis_client import sadd, sismember
sadd("KEY","VALUE")
assert sismember("KEY","VALUE")
