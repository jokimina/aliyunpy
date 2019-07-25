from aliyunsdkcore.request import RpcRequest
from .base import BaseAliyunApi


class DescribeDomainNamesRequest(RpcRequest):
    """
    WAF API: DescribeDomainNames
    Write due to lack of Aliyun WAF SDK
    """
    def __init__(self):
        RpcRequest.__init__(self, 'Waf', '2018-01-17', \
            'DescribeDomainNames', 'waf', protocol='https')

    def get_InstanceId(self):
        return self.get_query_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_query_param('InstanceId', InstanceId)

    def get_Region(self):
        return self.get_query_params().get('Region')

    def set_Region(self, Region):
        self.add_query_param('Region', Region)


class DescribeDomainConfigRequest(RpcRequest):
    """
    WAF API: DescribeDomainConfig
    Write due to lack of Aliyun WAF SDK
    """
    def __init__(self):
        RpcRequest.__init__(self, 'Waf', '2018-01-17', \
            'DescribeDomainConfig', 'waf', protocol='https')

    def get_InstanceId(self):
        return self.get_query_params().get('InstanceId')

    def set_InstanceId(self, InstanceId):
        self.add_query_param('InstanceId', InstanceId)

    def get_Region(self):
        return self.get_query_params().get('Region')

    def set_Region(self, Region):
        self.add_query_param('Region', Region)

    def get_Domain(self):
        return self.get_query_params().get('Domain')

    def set_Domain(self, Domain):
        self.add_query_param('Domain', Domain)


class AliyunWaf(BaseAliyunApi):
    """
    : Aliyun WAF related API
    """
    def get_domain_names(self, instance_id, region):
        request = DescribeDomainNamesRequest()
        request.set_InstanceId(instance_id)
        request.set_Region(region)
        result = self.client.do_action(request)
        return result

    def get_domain_config(self, instance_id, region, domain_name):
        request = DescribeDomainConfigRequest()
        request.set_InstanceId(instance_id)
        request.set_Region(region)
        request.set_Domain(domain_name)
        result = self.client.do_action(request)
        return result
