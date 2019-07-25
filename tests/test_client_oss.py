import json
from .base import BaseAliyunTestCase
from .config import suppress_warnings


class AliyunClientOnsTestCase(BaseAliyunTestCase):

    @suppress_warnings
    def test_list_bucket(self):
        r = self.client.oss.list_bucket()
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print(len(r))
