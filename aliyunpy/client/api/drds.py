from aliyunsdkdrds.request.v20171016 import (
    DescribeDrdsInstancesRequest, DescribeRegionsRequest
)
from .base import BaseAliyunApi


class AliyunDrds(BaseAliyunApi):
    def get_regions(self, id_only=False):
        """
        获取支持的region列表
        https://help.aliyun.com/document_detail/51129.html?spm=a2c4g.11186623.6.777.3af07cbdrI2FFq
        :param id_only: 是否只返回region id列表
        :return:
        """
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        result = self.client.do_action(request)
        result_list = result.get('DrdsRegions', {}).get('DrdsRegion', [])
        if id_only:
            result_list = list(set([x.get('RegionId') for x in result_list]))
        return result_list

    def list_drds(self, name_only=False, **kwargs):
        """
        获取实例列表信息
        https://help.aliyun.com/document_detail/51128.html?spm=a2c4g.11186623.6.776.263a6fefn8XahW
        :param name_only: 是否只返回实例名列表
        :param kwargs:
        :return:
        """
        result_list = []
        request = DescribeDrdsInstancesRequest.DescribeDrdsInstancesRequest()
        regions = self.get_regions(id_only=True)
        for region in regions:
            for k, v in kwargs.items():
                request.add_query_param(k, v)
            request.add_query_param('RegionId', region)
            result = self.client.do_action(request)
            result_list.extend(result.get('Data', {}).get('Instance', []))

        if name_only:
            result_list = [i['InstanceName'] for i in result_list]
        return result_list
