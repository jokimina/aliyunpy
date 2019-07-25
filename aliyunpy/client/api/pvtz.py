import copy
from aliyunsdkpvtz.request.v20180101 import (
    DescribeZonesRequest, DescribeZoneRecordsRequest
)
from .base import BaseAliyunApi


class AliyunDnsPrivateZone(BaseAliyunApi):
    def get_zones(self):
        """
        查询zone列表
        https://help.aliyun.com/document_detail/66243.html?spm=a2c4g.11186623.6.569.24fc6cc6L0G6Qs
        :return:
        """
        client = copy.deepcopy(self.client)
        client.acs_client.set_region_id('cn-hangzhou')
        request = DescribeZonesRequest.DescribeZonesRequest()
        request.set_PageSize(100)
        result = client.do_action(request)
        return result.get('Zones', {}).get('Zone', [])

    def list_zone_records(self, zoneid=None, **kwargs):
        """
        查询解析记录
        https://help.aliyun.com/document_detail/66252.html?spm=a2c4g.11186623.6.580.61a174bbMO2TSv
        :param zoneid: domain zone id, 不填遍历所有
        :param kwargs: 扩展参数
        :return:
        {
          "xxxx.com": [
            {
              "Status": "ENABLE",
              "Value": "127.0.0.1",
              "Rr": "private-test",
              "RecordId": 129807,
              "Ttl": 60,
              "Type": "A"
            }
          ]
        }
        """
        client = copy.deepcopy(self.client)
        client.acs_client.set_region_id('cn-hangzhou')

        result_dict = {}
        request = DescribeZoneRecordsRequest.DescribeZoneRecordsRequest()
        request.set_PageSize(100)
        request.set_PageNumber(1)
        for k, v in kwargs.items():
            request.add_query_param(k, v)

        zone_list = [zoneid] if zoneid else \
            [(x.get('ZoneId'), x.get('ZoneName')) for x in self.get_zones()]

        for x in zone_list:
            result_list = []
            zone_id, zone_name = x
            request.set_ZoneId(zone_id)
            result = client.do_action(request)
            total_count = float(result.get('TotalItems', 0))
            result_list.extend(result.get('Records').get('Record'))
            if not total_count:
                result_dict[zone_name] = result_list
                continue
            page_count = float(result.get('PageSize', 1))
            _p = total_count / page_count
            if _p > 1:
                for _p_num in range(2, int(_p) + 2):
                    request.set_PageNumber(_p_num)
                    result = client.do_action(request)
                    result_list.extend(result.get('ReCords').get('ReCord'))
            result_dict[zone_name] = result_list
        return result_dict
