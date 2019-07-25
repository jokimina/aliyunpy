import json
from .base import BaseAliyunTestCase


class AliyunClientRedisTestCase(BaseAliyunTestCase):

    def test_get_regions(self):
        r = self.client.redis.get_regions(id_only=True)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    def test_list_redis(self):
        r = self.client.redis.list_redis()
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print(len(r))
