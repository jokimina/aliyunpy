import json
from .base import BaseAliyunTestCase


class AliyunClientRdsTestCase(BaseAliyunTestCase):

    def test_get_regions(self):
        r = self.client.rds.get_regions(id_only=True)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    def test_list_rds(self):
        r = self.client.rds.list_rds()
        print(json.dumps(r, indent=2, ensure_ascii=False))
