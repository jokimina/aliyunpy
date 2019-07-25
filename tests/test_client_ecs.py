import re
import json
import httpretty
from aliyunpy.client import AliyunClient
from .config import auto_set_fixture
from .base import BaseAliyunTestCase


class AliyunClientEcsTestCase(BaseAliyunTestCase):

    @httpretty.activate
    @auto_set_fixture
    def test_list_ecs(self, fixture=None):
        p1 = fixture[0]
        p2 = fixture[1]
        httpretty.register_uri(httpretty.GET, re.compile(r'^.*\.aliyuncs\.com.*PageNumber=1.*$'), body=json.dumps(p1),
                               content_type='application/json', match_querystring=True)
        httpretty.register_uri(httpretty.GET, re.compile(r'^.*\.aliyuncs\.com.*PageNumber=2.*$'), body=json.dumps(p2),
                               content_type='application/json', match_querystring=True)
        r1 = self.client.ecs.list_ecs()
        self.assertEqual(101, len(r1))

        r2 = self.client.ecs.list_ecs(name_only=True)
        self.assertEqual(True, all([True if isinstance(x, str) else False for x in r2]))

    def test_list_ecs_all_region(self):
        r = self.client.ecs.list_ecs()
        print(len(r))


    def test_get_regions(self):
        r = self.client.ecs.get_regions(id_only=True)
        print(json.dumps(r, indent=2, ensure_ascii=False))
