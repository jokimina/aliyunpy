import json
from .base import BaseAliyunTestCase
from .config import suppress_warnings


class AliyunClientDnsPrivateZoneTestCase(BaseAliyunTestCase):

    @suppress_warnings
    def test_get_zones(self):
        r = self.client.pvtz.get_zones()
        print(json.dumps(r, indent=2, ensure_ascii=False))

    def test_list_zone_records(self):
        r = self.client.pvtz.list_zone_records()
        print(json.dumps(r, indent=2, ensure_ascii=False))
