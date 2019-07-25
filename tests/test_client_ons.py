import json
from .base import BaseAliyunTestCase


class AliyunClientOnsTestCase(BaseAliyunTestCase):

    def test_get_regions(self):
        r = self.client.ons.get_regions(id_only=True)
        print(json.dumps(r, indent=2, ensure_ascii=False))

    def test_get_instances(self):
        r = self.client.ons.get_instances()
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print(len(r))

    def test_list_topics(self):
        r = self.client.ons.list_topic(instance_id='MQ_INST_1726708279589269_yyyyy8Ak')
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print(len(r))

    def test_list_topic_all(self):
        r = self.client.ons.list_topic_all()
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print(len(r))
