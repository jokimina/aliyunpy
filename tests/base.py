import os
import unittest
import warnings
from aliyunpy.client import AliyunClient

warnings.filterwarnings("ignore")


class BaseAliyunTestCase(unittest.TestCase):
    access_key = os.getenv('ACCESS_KEY') or '111111'
    access_secret = os.getenv('ACCESS_SECRET') or '222222'

    def setUp(self):
        self.client = AliyunClient(access_key=self.access_key, access_secret=self.access_secret)
