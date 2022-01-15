import asyncio
import typing
import aioredis
import simplejson as json


class RedisCart:

    def __init__(self, host: str = 'localhost', port=6379, db=None, password=None,
                 ssl=None, pool_size=10, loop=None, prefix='items',
                 data_ttl: int = 0,
                 bucket_ttl: int = 0,
                 **kwargs):
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._ssl = ssl
        self._pool_size = pool_size
        self._loop = loop or asyncio.get_event_loop()
        self._kwargs = kwargs
        self._prefix = (prefix,)
        self._data_ttl = data_ttl
        self._bucket_ttl = bucket_ttl

        self._redis: typing.Optional[aioredis.RedisConnection] = None
        self._connection_lock = asyncio.Lock(loop=self._loop)

    async def redis(self) -> aioredis.Redis:
        """
        Get Redis connection
        """
        # Use thread-safe asyncio Lock because this method without that is not safe
        async with self._connection_lock:
            if self._redis is None or self._redis.closed:
                self._redis = await aioredis.create_redis_pool((self._host, self._port),
                                                               db=self._db, password=self._password, ssl=self._ssl,
                                                               minsize=1, maxsize=self._pool_size,
                                                               loop=self._loop, **self._kwargs)
        return self._redis

    def generate_key(self, *parts):
        return ':'.join(self._prefix + tuple(map(str, parts)))

    async def close(self):
        async with self._connection_lock:
            if self._redis and not self._redis.closed:
                self._redis.close()

    async def wait_closed(self):
        async with self._connection_lock:
            if self._redis:
                return await self._redis.wait_closed()
            return True

    @classmethod
    def check_address(cls, *, user: typing.Union[str, int, None] = None) -> typing.Union[str, int]:

        if user is None:
            raise ValueError('User Id is required')
        return user

    async def set_data(self, *, user: typing.Union[str, int, None] = None,
                       data: typing.Dict = None):
        user = self.check_address(user=user)
        key = self.generate_key(user)
        redis = await self.redis()
        await redis.set(key, json.dumps(data), expire=self._data_ttl)

    async def get_data(self, *, user: typing.Union[str, int, None] = None,
                       default: typing.Optional[dict] = None) -> typing.Dict:
        user = self.check_address(user=user)
        key = self.generate_key(user)
        redis = await self.redis()
        raw_result = await redis.get(key, encoding='utf8')
        if raw_result:
            return json.loads(raw_result)
        return default or {}


shopcart = RedisCart()
