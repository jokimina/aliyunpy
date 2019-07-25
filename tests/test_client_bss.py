import json
import datetime
import httpretty
from .base import BaseAliyunTestCase
from .config import auto_load_fixture, suppress_warnings


class AliyunClientBssTestCase(BaseAliyunTestCase):
    def test_query_bill(self):
        r = self.client.bss.query_bill('2019-01')
        print(len(r))
        print(sum([x['PaymentAmount'] for x in r]))
        # print(json.dumps(r, ensure_ascii=False))

    def test_query_bill_overview(self):
        r = self.client.bss.query_bill_overview('2019-01')
        print(json.dumps(r, ensure_ascii=False))

    def test_query_instance_bill(self):
        r = self.client.bss.query_instance_bill('2019-01', ProductCode='ecs', SubscriptionType='Subscription',
                                                PageSize=100)
        print(json.dumps(r, ensure_ascii=False))

    def test_query_instance_gaap_cost(self):
        r = self.client.bss.query_instance_gaap_cost(billing_cycle='2019-01')
        print(json.dumps(r, ensure_ascii=False))

    def test_query_order(self):
        # tz_utc_8 = datetime.timezone(datetime.timedelta(hours=0))

        order_cycle = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
        # r = self.client.bss.query_orders(CreateTimeStart=order_cycle)
        r = self.client.bss.query_order(CreateTimeStart='2019-01-01T00:00:00Z', CreateTimeEnd='2019-02-01T00:00:00Z')
        print(len(r))
        print(sum([x['PretaxAmount'] for x in r]))
        # print(json.dumps(r, ensure_ascii=False))

    def test_get_order_detail(self):
        r = self.client.bss.get_order_detail('203269617950649')
        print(json.dumps(r, ensure_ascii=False))
