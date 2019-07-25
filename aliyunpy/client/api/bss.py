import time
import datetime
from aliyunsdkbssopenapi.request.v20171214 import QueryBillOverviewRequest, QueryBillRequest, \
    QueryInstanceBillRequest, QueryInstanceGaapCostRequest, \
    QueryOrdersRequest, GetOrderDetailRequest
from .base import BaseAliyunApi
from ..utils import date_to_isoformat_datetime, isoformat_to_datetime, get_logger

__doc__ = """
账单类型：SubscriptionOrder (预付订单)， PayAsYouGoBill (后付账单)， Refund (退款)， Adjustment (调账)
"""

logger = get_logger(__file__)


class AliyunBss(BaseAliyunApi):
    def query_bill(self, billing_cycle=None, product_code=None, \
                   billing_type=None, delay=3, count_only=False, **kwargs):
        """
        查询用户某个账期内结算账单, 默认返回所有
        https://help.aliyun.com/document_detail/100392.html?spm=a2c4g.11186623.6.591.24bd256406Dfsh

        :param product_code: 产品代码
        :param billing_type: 类型SubscriptionOrder／PayAsYouGoBill／Refund／Adjustment
        :param billing_cycle: 账期，YYYY-MM。样例：2018-07
        :param delay: 请求延时间隔, 防止被api限流
        """
        result_list = []
        request = QueryBillRequest.QueryBillRequest()
        request.set_PageSize(100)
        request.set_BillingCycle(billing_cycle)
        if product_code:
            request.set_ProductCode(product_code)
        if billing_type:
            request.set_Type(billing_type)
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        data = result.get('Data', {})
        result_list.extend(data.get("Items", {}).get("Item", []))
        total_count = float(data.get('TotalCount', 0))
        if count_only:
            return total_count
        page_count = float(data.get('PageSize', 1))
        _p = total_count / page_count
        if _p > 1:
            for _p_num in range(2, int(_p) + 2):
                # 超过10页就延长请求间隔, 防止触发限流
                if _p > 10:
                    time.sleep(delay)
                request.set_PageNum(_p_num)
                logger.info('total page %s, now query %s.', (int(_p) + 1), _p_num)
                result = self.client.do_action(request)
                data = result.get('Data', {})
                result_list.extend(data.get('Items', {}).get('Item', []))
        return result_list

    def query_bill_overview(self, billing_cycle=None, **kwargs):
        """
        查询用户某个账期内账单总览信息。
        https://help.aliyun.com/document_detail/100389.html?spm=a2c4g.11186623.6.590.370e534foaqg3K

        :param billing_cycle: 账期，YYYY-MM。样例：2018-07
        """
        result_list = []
        request = QueryBillOverviewRequest.QueryBillOverviewRequest()
        request.set_BillingCycle(billing_cycle)
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        result_list.extend(result.get('Data', {}).get('Items', {}).get('Item', []))
        return result_list

    def query_instance_bill(self, billing_cycle=None, **kwargs):
        """
        查询用户某个账期内所有商品实例的消费汇总信息。
        https://help.aliyun.com/document_detail/100392.html?spm=a2c4g.11186623.6.591.24bd256406Dfsh

        :param billing_cycle: 账期，YYYY-MM。样例：2018-07
        """
        result_list = []
        request = QueryInstanceBillRequest.QueryInstanceBillRequest()
        request.set_PageSize(100)
        request.set_BillingCycle(billing_cycle)
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        data = result.get('Data', {})
        result_list.extend(data.get("Items", {}).get("Item", []))
        total_count = float(data.get('TotalCount', 0))
        page_count = float(data.get('PageSize', 1))
        _p = total_count / page_count
        if _p > 1:
            for _p_num in range(2, int(_p) + 2):
                request.set_PageNum(_p_num)
                result = self.client.do_action(request)
                data = result.get('Data', {})
                result_list.extend(data.get('Items', {}).get('Item', []))
        return result_list

    def query_instance_gaap_cost(self, billing_cycle=None, **kwargs):
        """
        查询实例的月费用分摊
        注：每月初4号中午12:00后可拉取上月全量GAAP账单，此时间前拉取GAAP账单可能不全。
        https://help.aliyun.com/document_detail/87995.html?spm=a2c4g.11186623.6.593.e5de3f80fLqEW2

        :param billing_cycle: 账期，YYYY-MM。样例：2018-07
        """
        request = QueryInstanceGaapCostRequest.QueryInstanceGaapCostRequest()
        request.set_BillingCycle(billing_cycle)
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def query_order(self, **kwargs):
        """
        查询用户或者分销客户订单列表情况, 缺省查询当前时间最近1小时内订单
        https://help.aliyun.com/document_detail/89079.html?spm=a2c4g.11186623.6.603.373f534f8yL3Zp
        """
        result_list = []
        request = QueryOrdersRequest.QueryOrdersRequest()
        request.set_PageSize(100)
        for k, v in kwargs.items():
            if isinstance(v, datetime.date):
                v = date_to_isoformat_datetime(v)
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        data = result.get('Data', {})
        result_list.extend(data.get("OrderList", {}).get("Order", []))
        total_count = float(data.get('TotalCount', 0))
        page_count = float(data.get('PageSize', 1))
        _p = total_count / page_count
        if _p > 1:
            for _p_num in range(2, int(_p) + 2):
                request.set_PageNum(_p_num)
                result = self.client.do_action(request)
                data = result.get('Data', {})
                result_list.extend(data.get('OrderList', {}).get('Order', []))
        for i, item in enumerate(result_list):
            for k, v in item.items():
                if 'Time' in k:
                    result_list[i][k] = isoformat_to_datetime(v).strftime("%Y-%m-%d %H:%M:%S")
        return result_list

    def get_order_detail(self, order_id=None, delay=None):
        """
        查询用户或分销客户某个订单详情信息
        https://help.aliyun.com/document_detail/89084.html?spm=a2c4g.11186623.6.604.67fc6ff0KxXDNn
        :param order_id: 订单号
        :param delay: 请求延时间隔, 防止被api限流
        """
        if delay:
            time.sleep(delay)
        request = GetOrderDetailRequest.GetOrderDetailRequest()
        request.set_OrderId(order_id)
        result = self.client.do_action(request)
        result = result.get('Data', {}).get('OrderList', {}).get('Order', [])
        result = result[0] if result else result
        for k, v in result.items():
            if 'Time' in k:
                result[k] = isoformat_to_datetime(v).strftime("%Y-%m-%d %H:%M:%S")
        return result
