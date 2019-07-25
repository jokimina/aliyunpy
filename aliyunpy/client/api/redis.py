import string
import time
from random import choice
from aliyunsdkr_kvstore.request.v20150101 import (
    CreateInstanceRequest, DescribeRegionsRequest,
    DescribeInstancesRequest
)
from .base import BaseAliyunApi


class AliyunRedis(BaseAliyunApi):
    def get_regions(self, id_only=False):
        """
        获取支持的region列表
        https://help.aliyun.com/document_detail/61012.html?spm=a2c4g.11186623.6.687.2b10ae6dPxXy2S
        :param id_only: 是否只返回region id列表
        :return:
        """
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        result = self.client.do_action(request)
        result_list = result.get('RegionIds', {}).get('KVStoreRegion', [])
        if id_only:
            result_list = list(set([x.get('RegionId') for x in result_list]))
        return result_list

    def list_redis(self, name_only=False, **kwargs):
        """
        获取实例列表信息
        https://help.aliyun.com/document_detail/60933.html?spm=a2c4g.11186623.6.694.67002cacaswc5I
        :param name_only:
        :param kwargs:
        :return:
        """
        result_list = []
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        regions = self.get_regions(id_only=True)
        for region in regions:
            request.set_PageSize(100)
            request.set_PageNumber(1)
            for k, v in kwargs.items():
                request.add_query_param(k, v)
            request.add_query_param('RegionId', region)
            result = self.client.do_action(request)
            result_list.extend(result.get('Instances', {}).get('KVStoreInstance', []))

            total_count = float(result.get('TotalCount', 0))
            if not total_count:
                continue
            page_count = float(result.get('PageSize', 1))
            _p = total_count / page_count
            if _p > 1:
                for _p_num in range(2, int(_p) + 2):
                    request.set_PageNumber(_p_num)
                    result = self.client.do_action(request)
                    result_list.extend(result.get('Instances', {}).get('KVStoreInstance', []))
            # 防止被限流
            time.sleep(1)
        if name_only:
            result_list = [i['InstanceName'] for i in result_list]
        return result_list

    def create_redis_instance(self, **kwargs):
        request = CreateInstanceRequest.CreateInstanceRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_redis_instance_mini(self, **kwargs):
        """
        :return: result && password
        """
        base_str = string.digits + string.ascii_letters
        _password = ''.join([choice(base_str) \
                for _ in range(30)])
        params = {
            #'InstanceClass': 'redis.logic.splitrw.small.1db.3rodb.4proxy.default',
            'InstanceClass': 'redis.master.small.default',
            'Password': _password,
            'NetworkType': 'VPC',
            'InstanceType': 'Redis',
            'ChargeType': 'PrePaid',
            'Period': 1,
            'EngineVersion': '2.8',
            }
        kwargs.update(params)
        result = self.create_redis_instance(**kwargs)
        result.update({'Password': _password})
        return result
