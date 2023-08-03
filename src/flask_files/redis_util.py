import redis
from src.flask_files.config import Config


class RedisCache:

    def __init__(self):
        self.redis_client = None

    def init_redis_client(self):
        self.redis_client = redis.Redis(
            host='redis-17278.c73.us-east-1-2.ec2.cloud.redislabs.com',
            port=17278,
            password=Config.redis_password)

    def get_client(self) -> redis.Redis:
        return self.redis_client


redis_client = RedisCache()

