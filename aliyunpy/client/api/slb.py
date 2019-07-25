from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest, \
    DescribeListenerAccessControlAttributeRequest, \
    DescribeLoadBalancerAttributeRequest, DescribeHealthStatusRequest, \
    DescribeRulesRequest, DescribeRuleAttributeRequest, \
    DescribeVServerGroupsRequest, DescribeVServerGroupAttributeRequest, \
    CreateLoadBalancerRequest, DescribeRegionsRequest, \
    SetLoadBalancerTCPListenerAttributeRequest
from .base import BaseAliyunApi


class AliyunSlb(BaseAliyunApi):
    """
    阿里云SLB负载均衡相关API
        获取实例列表；
        获取指定实例配置；
        获取指定实例后端不健康主机实例ID列表；
        获取指定端口转发规则列表或指定规则；
    """

    def get_regions(self, id_only=False):
        """
        获取支持的region列表
        https://help.aliyun.com/document_detail/27584.html?spm=a2c4g.11174283.6.633.58ef11925XsImC
        :param id_only: 是否只返回region id列表
        :return:
        """
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        result = self.client.do_action(request)
        result_list = result.get('Regions', {}).get('Region', [])
        if id_only:
            result_list = list(set([x.get('RegionId') for x in result_list]))
        return result_list

    def list_slb(self, name_only=False, **kwargs):
        """
        获取实例列表信息
        https://help.aliyun.com/document_detail/27582.html?spm=a2c4g.11186623.6.631.424952e51QEPuJ
        :param name_only:
        :param kwargs:
        :return:
        """
        result_list = []
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        regions = self.get_regions(id_only=True)
        for region in regions:
            request.set_PageSize(100)
            request.set_PageNumber(1)
            for k, v in kwargs.items():
                request.add_query_param(k, v)
            request.add_query_param('RegionId', region)
            result = self.client.do_action(request)
            result_list.extend(result.get('LoadBalancers', {}).get('LoadBalancer', []))

            total_count = float(result.get('TotalCount', 0))
            if not total_count:
                continue
            page_count = float(result.get('PageSize', 1))
            _p = total_count / page_count
            if _p > 1:
                for _p_num in range(2, int(_p) + 2):
                    request.set_PageNumber(_p_num)
                    result = self.client.do_action(request)
                    result_list.extend(result.get('LoadBalancers').get('LoadBalancer'))

        if name_only:
            result_list = [i['InstanceName'] for i in result_list]
        return result_list

    def get_slb_list(self):
        """
        :return: SLB实例列表
        """
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        result = self.client.do_action(request)['LoadBalancers']['LoadBalancer']
        return result

    def get_slb_config(self, slb_id):
        """
        :params:
            SLB实例ID
        :return:
            SLB ID对应实例配置字典
        """
        request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slb_id)
        result = self.client.do_action(request)
        return result

    def get_listener_whitelist(self, slb_id, listener_port):
        """
        :params:
            SLB实例ID 前端监听端口号
        :return:
            白名单列表字符串
        """
        request = DescribeListenerAccessControlAttributeRequest \
            .DescribeListenerAccessControlAttributeRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slb_id)
        request.set_ListenerPort(listener_port)
        result = self.client.do_action(request)
        # pylint:disable=C0303
        return result['SourceItems'] \
            if result['AccessControlStatus'] == \
               'open_white_list' else None

    def get_unhealthy_backends(self, slb_id, listener_port):
        """
        :params:
            SLB实例ID 前端监听端口号
        :return:
            后端不健康实例ID列表
        """
        request = DescribeHealthStatusRequest.DescribeHealthStatusRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slb_id)
        request.set_ListenerPort(listener_port)
        result = self.client \
            .do_action(request)['BackendServers']['BackendServer']
        return [backend['ServerId'] for backend in result \
                if backend['ServerHealthStatus'] == 'abnormal']

    def get_redirect_rules(self, slb_id, listener_port, rule_id='all'):
        """
        :params:
            SLB实例ID 后端监听端口号 转发规则ID
        :return:
            转发规则列表
        默认返回当前监听端口所有转发规则列表；
        指定ID返回指定规则字典；
        """
        if rule_id == 'all':
            request = DescribeRulesRequest.DescribeRulesRequest()
            request.set_accept_format('json')
            request.set_LoadBalancerId(slb_id)
            request.set_ListenerPort(listener_port)
            result = self.client.do_action(request)['Rules']['Rule']
            return result
        request = DescribeRuleAttributeRequest.DescribeRuleAttributeRequest()
        request.set_accept_format('json')
        request.set_RuleId(rule_id)
        result = self.client.do_action(request)
        return result

    def get_vgroups(self, slb_id):
        """
        :params: SLB ID
        :return: 返回当前SLB实例虚拟组列表
        """
        request = DescribeVServerGroupsRequest \
            .DescribeVServerGroupsRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slb_id)
        result = self.client.do_action(request)['VServerGroups']['VServerGroup']
        return result

    def get_vgroups_attributes(self, slb_id):
        """
        :params: SLB ID
        :return: 返回指定SLB下虚拟组详情列表
        """
        vgroup_attr_list = []
        slb_vgroups = self.get_vgroups(slb_id)
        request = DescribeVServerGroupAttributeRequest. \
            DescribeVServerGroupAttributeRequest()
        request.set_accept_format('json')
        for vgroup in slb_vgroups:
            request.set_VServerGroupId(vgroup['VServerGroupId'])
            result = self.client.do_action(request)
            result.pop('RequestId')
            vgroup_attr_list.append(result)
        return vgroup_attr_list

    def create_slb(self, **kwargs):
        request = CreateLoadBalancerRequest.CreateLoadBalancerRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_slb_mini(self, **kwargs):
        params = {
            'Bandwidth': 1,
            'InternetChargeType': 'paybytraffic',
            'LoadBalancerSpec': 'slb.s1.small',
            'PayType': 'PayOnDemand'
        }
        kwargs.update(params)
        # pylint: disable=E1121
        result = self.create_slb(**kwargs)
        return result

    def set_tcp_listener_attr(self, **kwargs):
        """
        设置SLB TCP监听属性
        https://help.aliyun.com/document_detail/27604.html?spm=a2c4g.11186623.6.645.7e0de5afZXm5kS
        """
        request = SetLoadBalancerTCPListenerAttributeRequest\
            .SetLoadBalancerTCPListenerAttributeRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result
