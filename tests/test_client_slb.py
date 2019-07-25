import json
from .base import BaseAliyunTestCase


class AliyunClientSlbTestCase(BaseAliyunTestCase):

    def test_get_regions(self):
        r = self.client.slb.get_regions(id_only=True)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    def test_list_slb(self):
        r = self.client.slb.list_slb()
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print(len(r))
