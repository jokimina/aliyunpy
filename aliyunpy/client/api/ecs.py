from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, \
    CreateInstanceRequest, StartInstanceRequest, \
    RebootInstanceRequest, \
    DescribeEipAddressesRequest, \
    AllocateEipAddressRequest, AllocatePublicIpAddressRequest, \
    AssociateEipAddressRequest, UnassociateEipAddressRequest, \
    ModifyInstanceAttributeRequest, DescribeRegionsRequest
from .base import BaseAliyunApi


# pylint: disable=E1121


class AliyunEcs(BaseAliyunApi):
    def get_regions(self, id_only=False):
        """
        获取支持的region列表
        https://help.aliyun.com/document_detail/25609.html
        :param id_only: 是否只返回region id列表
        :return:
        """
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        result = self.client.do_action(request)
        result_list = result.get('Regions', {}).get('Region', [])
        if id_only:
            # pylint: disable=R1718
            result_list = list(set([x.get('RegionId') for x in result_list]))
        return result_list

    def list_ecs(self, name_only=False, **kwargs):
        """
        获取实例列表信息
        https://help.aliyun.com/document_detail/25506.html?spm=a2c4g.11186623.6.941.2b453215sQTZIS
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
            result_list.extend(result.get('Instances', {}).get('Instance'))

            total_count = float(result.get('TotalCount', 0))
            if not total_count:
                continue
            page_count = float(result.get('PageSize', 1))
            _p = total_count / page_count
            if _p > 1:
                for _p_num in range(2, int(_p) + 2):
                    request.set_PageNumber(_p_num)
                    result = self.client.do_action(request)
                    result_list.extend(result.get('Instances').get('Instance'))

        if name_only:
            result_list = [i['InstanceName'] for i in result_list]
        return result_list

    def get_ecs_proxy(self, name_only=False, **kwargs):
        """
        :return: ecs instance with tag: instance_category=proxy
        """
        proxy_list = []
        proxy_tag = {'TagKey': 'instance_category', 'TagValue': 'proxy'}
        result_list = self.list_ecs(**kwargs)
        for result in result_list:
            if 'Tags' in result.keys():
                if proxy_tag in result['Tags']['Tag']:
                    if name_only:
                        proxy_list.append(result['InstanceName'])
                    else:
                        proxy_list.append(result)
        return proxy_list

    def create_ecs(self, **kwargs):
        """
        :return: ECS创建实例ID
        """
        request = CreateInstanceRequest.CreateInstanceRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def restart_ecs(self, **kwargs):
        """
        : 重启ECS实例
        """
        request = RebootInstanceRequest.RebootInstanceRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def start_ecs(self, **kwargs):
        """
        :params: ECS实例ID
        """
        request = StartInstanceRequest.StartInstanceRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def start_batch_ecs(self, instance_ids, **kwargs):
        """
        :params: Instance ID列表
        """
        results = []
        for instance_id in instance_ids:
            result = self.start_ecs(InstanceId=instance_id, **kwargs)
            results.append(result)
        return results

    def create_ecs_proxy(self, **kwargs):
        """
        :params: 爬虫交换机ID
        """
        params = {
            'InstanceType': 'ecs.t5-lc2m1.nano',
            'IoOptimized': 'optimized',
            'ImageId': 'ubuntu_16_0402_64_20G_alibase_20171227.vhd',
            'KeyPairName': 'admin',
            'Tag.1.Key': 'instance_category',
            'Tag.1.Value': 'proxy',
            'InstanceChargeType': 'PrePaid',
            'Period': 1,
            'PeriodUnit': 'Month',
            'AutoRenew': True,
            'InternetMaxBandwidthOut': 1,
            'AutoRenewPeriod': 1
        }
        kwargs.update(params)
        result = self.create_ecs(**kwargs)
        return result

    def create_ecs_proxys(self, num=1, **kwargs):
        """
        :params: proxy ECS数量
        """
        results = []
        for _ in range(num):
            result = self.create_ecs_proxy(**kwargs)
            results.append(result)
        return results

    def create_ecs_mini(self, **kwargs):
        """
        :params: 交换机ID
        """
        params = {
            'InstanceType': 'ecs.g5.xlarge',
            'IoOptimized': 'optimized',
            'ImageId': 'ubuntu_16_0402_64_20G_alibase_20171227.vhd',
            'KeyPairName': 'admin',
            'InstanceChargeType': 'PrePaid',
            'Period': 1,
            'PeriodUnit': 'Month',
            'AutoRenew': True,
            'AutoRenewPeriod': 1
        }
        kwargs.update(params)
        result = self.create_ecs(**kwargs)
        if 'InstanceId' not in result.keys():
            raise KeyError('InstanceId')
        start_result = self.start_ecs(InstanceId=result['InstanceId'])
        return start_result

    def list_eip(self, **kwargs):
        result_list = []
        request = DescribeEipAddressesRequest.DescribeEipAddressesRequest()
        request.set_PageSize(50)
        regions = self.get_regions(id_only=True)
        for region in regions:
            request.set_PageNumber(1)
            for k, v in kwargs.items():
                request.add_query_param(k, v)
            request.add_query_param('RegionId', region)
            result = self.client.do_action(request)
            result_list.extend(result.get(\
                'EipAddresses', {}).get(\
                'EipAddress', []))
            total_count = float(result.get('TotalCount', 0))
            if not total_count:
                continue
            page_count = float(result.get('PageSize', 1))
            _p = total_count / page_count
            if _p > 1:
                for _p_num in range(2, int(_p) + 2):
                    request.set_PageNumber(_p_num)
                    result = self.client.do_action(request)
                    result_list.extend(result.get(\
                        'EipAddresses', {}).get(\
                        'EipAddress', []))
        return result_list

    def create_eip(self, **kwargs):
        """
        :return: 创建EIP及ID
        """
        request = AllocateEipAddressRequest.AllocateEipAddressRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_batch_eip(self, num=1, **kwargs):
        """
        :return: 创建EIP及ID列表
        """
        results = []
        params = {
            'Bandwidth': 5,
            'InternetChargeType': 'PayByTraffic',
        }
        kwargs.update(params)
        for _ in range(num):
            result = self.create_eip(**kwargs)
            results.append(result)
        return results

    def associate_eip(self, instance_id, eip_id, instance_type='Ecs'):
        """
        :params: ECS ID, EIP IP
        :return: 绑定结果
        """
        if instance_type not in ['Nat', 'Slb', 'Ecs']:
            raise TypeError('Wrong instance type.')
        request = AssociateEipAddressRequest.AssociateEipAddressRequest()
        request.set_InstanceType(instance_type)
        request.set_InstanceId(instance_id)
        request.set_AllocationId(eip_id)
        result = self.client.do_action(request)
        return result

    def associate_ecs_eip(self, ecs_id, eip_id):
        """
        :params: ECS实例ID & EIP ID
        """
        result = self.associate_eip(ecs_id, eip_id)
        return result

    def associate_nat_eip(self, nat_gateway_id, eip_id):
        """
        :params: NAT网关ID & EIP ID
        """
        result = self.associate_eip(nat_gateway_id, \
                                    eip_id, instance_type='Nat')
        return result

    def unassociate_ecs_eip(self, ecs_id, eip_id):
        """
        :return: EIP解绑结果
        """
        request = UnassociateEipAddressRequest.UnassociateEipAddressRequest()
        request.set_InstanceType("EcsInstance")
        request.set_InstanceId(ecs_id)
        request.set_AllocationId(eip_id)
        result = self.client.do_action(request)
        return result

    def modify_instance_attr(self, instance_id=None, **kwargs):
        """
        修改实例信息
        https://help.aliyun.com/document_detail/25503.html?spm=a2c4g.11174283.6.950.3c5b52feWdhQnd

        :param instance_id:
        :param kwargs:
        """
        request = ModifyInstanceAttributeRequest.ModifyInstanceAttributeRequest()
        request.set_InstanceId(instance_id)
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def modify_instance_name(self, instance_ids, name_prefix, start_index=1):
        results = []
        for i in instance_ids:
            _index = start_index + instance_ids.index(i)
            _index_id = str(_index) if _index > 9 else "0{}".format(_index)
            instance_name = "{}{}".format(name_prefix, _index_id)
            result = self.modify_instance_attr(
                i,
                InstanceName=instance_name,
                HostName=instance_name)
            results.append(result)
        return results

    def allocate_pub_ip(self, **kwargs):
        """
        :params: ECS实例ID
        """
        request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result
