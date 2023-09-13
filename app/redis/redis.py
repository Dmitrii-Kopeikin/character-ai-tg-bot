from redis.asyncio.client import Redis

from config import config


redis = Redis.from_url(config.redis.url)
