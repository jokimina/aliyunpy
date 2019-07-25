from .base import BaseAliyunTestCase


class AliyunClientTestCase(BaseAliyunTestCase):
    def test_acs_client(self):
        self.assertEqual(self.client._acs_client.get_access_key(), self.access_key)
        self.assertEqual(self.client._acs_client.get_access_secret(), self.access_secret)
