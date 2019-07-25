import json
from .base import BaseAliyunTestCase


class AliyunClientDrdsTestCase(BaseAliyunTestCase):

    def test_get_regions(self):
        r = self.client.drds.get_regions(id_only=True)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    def test_list_drds(self):
        r = self.client.drds.list_drds()
        print(json.dumps(r, indent=2, ensure_ascii=False))
