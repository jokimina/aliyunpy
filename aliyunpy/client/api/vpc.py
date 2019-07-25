#-*- coding:utf-8 -*-
from aliyunsdkvpc.request.v20160428 import DescribeVpcsRequest, \
        DescribeVSwitchesRequest, \
        DescribeVRoutersRequest, DescribeRouteTablesRequest, \
        DescribeNatGatewaysRequest, DescribeSnatTableEntriesRequest, \
        CreateVpcRequest, CreateVSwitchRequest, \
        CreateNatGatewayRequest, CreateBandwidthPackageRequest, \
        CreateSnatEntryRequest
from .base import BaseAliyunApi


class AliyunVpc(BaseAliyunApi):
    """
    阿里云VPC相关API：
        VPC,
        Vswitch(虚拟交换机),
        VRouter(虚拟路由器),
        VRouter Table(路由表),
        NAT Gateway, bandwidth package, SNAT
        相关资源信息获取及创建；
    """

    def get_vpc_list(self):
        """
        :return: 当前可用区下VPC列表
        """
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_accept_format('json')
        result = self.client.do_action(request)['Vpcs']['Vpc']
        return result

    def get_vswitch_list(self, vpc_id):
        """
        :params: VPC实例ID
        :return: 指定VPC下虚拟交换机Vswitch列表
        默认页显示50；
        """
        request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
        request.set_accept_format('json')
        request.set_PageSize(50)
        request.set_VpcId(vpc_id)
        result = self.client.do_action(request)['VSwitches']['VSwitch']
        return result

    def get_vrouter_list(self, vrouter_id='all'):
        """
        :params: Vrouter虚拟路由器ID
        :return: 默认返回路由器列表
                 指定id返回对应路由器字典；
        默认页显示50；
        """
        request = DescribeVRoutersRequest.DescribeVRoutersRequest()
        request.set_accept_format('json')
        request.set_PageSize(50)
        if vrouter_id == 'all':
            return self.client.do_action(request)['VRouters']['VRouter']
        request.set_VRouterId(vrouter_id)
        return self.client.do_action(request)['VRouters']['VRouter'][0]

    def get_vroute_table(self, vrouter_id):
        """
        :params: Vrouter虚拟路由器ID
        :return: 路由表规则列表
        默认页显示50；
        """
        request = DescribeRouteTablesRequest.DescribeRouteTablesRequest()
        request.set_accept_format('json')
        request.set_PageSize(50)
        request.set_VRouterId(vrouter_id)
        return self.client.do_action(request)['RouteTables']['RouteTable']

    def get_nat_gateways(self, nat_gateway_id='all'):
        """
        :params: Nat网关ID
        :return: 默认Nat网关列表 指定ID返回对应网关信息
        默认也显示50；
        """
        request = DescribeNatGatewaysRequest.DescribeNatGatewaysRequest()
        request.set_accept_format('json')
        request.set_PageSize(50)
        if nat_gateway_id == 'all':
            return self.client.do_action(request)['NatGateways']['NatGateway']
        request.set_NatGatewayId(nat_gateway_id)
        return self.client.do_action(request)['NatGateways']['NatGateway'][0]

    def get_nat_gateway_eiplist(self, nat_gateway_id='all'):
        """
        :params: Nat网关ID
        :return: 返回NAT网关IP列表
        """
        nat_gateway = self.get_nat_gateways(nat_gateway_id)
        if isinstance(nat_gateway, list):
            result = [ip['IpAddress'] for nat in nat_gateway \
                    for ip in nat['IpLists']['IpList']]
        elif isinstance(nat_gateway, dict):
            result = [ip['IpAddress'] for ip in nat_gateway['IpLists']['IpList']]
        else:
            result = None
        return result

    def get_nat_bandwidthlist(self, nat_gateway_id='all'):
        """
        :params: Nat网关ID
        :return: 返回NAT网关带宽包ID列表
        """
        nat_gateway = self.get_nat_gateways(nat_gateway_id)
        if isinstance(nat_gateway, list):
            bandwidthlist = []
            for nat in nat_gateway:
                bandwidthlist.extend(nat['BandwidthPackageIds']['BandwidthPackageId'])
            result = bandwidthlist
        elif isinstance(nat_gateway, dict):
            result = nat_gateway['BandwidthPackageIds']['BandwidthPackageId']
        else:
            result = None
        return result

    def get_snat_table_ids(self, nat_gateway_id='all'):
        """
        :params: NAT网关ID
        :return: SNAT表ID列表
        """
        nat_gateway = self.get_nat_gateways(nat_gateway_id)
        if isinstance(nat_gateway, list):
            snat_table_idlist = []
            for nat in nat_gateway:
                snat_table_idlist.extend(nat['SnatTableIds']['SnatTableId'])
            snat_table_ids = snat_table_idlist
        elif isinstance(nat_gateway, dict):
            snat_table_ids = nat_gateway['SnatTableIds']['SnatTableId']
        else:
            snat_table_ids = None
        return snat_table_ids

    def get_snat_table_entries(self, snat_table_id):
        """
        :params: SNAT表ID
        :return: 返回SNAT表条目列表
        """
        request = DescribeSnatTableEntriesRequest\
                .DescribeSnatTableEntriesRequest()
        request.set_accept_format('json')
        request.set_PageSize(50)
        request.set_SnatTableId(snat_table_id)
        result = self.client\
                .do_action(request)['SnatTableEntries']['SnatTableEntry']
        return result

    # pylint: disable=C0303 
    def create_vpc(self, **kwargs):
        """
        https://help.aliyun.com/document_detail/\
                35737.html?spm=a2c4g.11174283.6.603.2cc96dd4NCrbSa
        :params:
            {
                'RegionId': '可用区ID',
                'VpcName': 'Vpc名',
                'CidrBlock': [
                    '10.0.0.0/8',
                    '172.16.0.0/12',
                    '192.168.0.0/16'
                    ],
                'EnableIpv6': False,
                'Ipv6CidrBlock': '223.223.213.122',
                'Description': '描述',
            }
        :return:
            VPC ID, VRouter ID, RouterTable ID
        """
        request = CreateVpcRequest.CreateVpcRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_vswitch(self, **kwargs):
        """
        :params:
            {
                'VpcId': 'VPC ID',
                'RegionId': '可用区',
                'ZoneId': '所属区ID',
                'VSwitchName': '交换机名字',
                'CidrBlock': 'IPv4网段',
                'Ipv6CidrBlock': 'IPv6网段',
                'Description': '描述',
            }
        """
        request = CreateVSwitchRequest.CreateVSwitchRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_nat_gateway(self, **kwargs):
        """
        :params:
            {
                'VpcId': 'VPC ID',
                'RegionId': '可用区ID',
                'Name': '网关名',
                'Spec': [
                    'Small',
                    'Middle',
                    'Large',
                    'XLarge'
                    ],
                'Description': '描述',
            }
        :return:
            NatGatewayId, ForwardTableIds,
            SnatTableIds, SnatTableIds
        """
        request = CreateNatGatewayRequest.CreateNatGatewayRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_bandwidth_pkg(self, **kwargs):
        """
        :params:
            {
                'NatGatewayId': 'NAT网关ID',
                'RegionId': '可用区ID',
                'Name': '带宽包名',
                'Bandwidth': '5',
                'IpCount': '1,2',
                'InternetChargeType': 'PayByTraffic',
                'Zone': 'cn-qingdao-a',
                'Description': '描述',
            }
        """
        request = CreateBandwidthPackageRequest\
                .CreateBandwidthPackageRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_snat_entry(self, **kwargs):
        """
        :params:
            {
                'RegionId': '可用区ID',
                'SnatIp': 'SNAT IP',
                'SnatTableId': 'SNAT表ID',
                'SourceVSwitchId': '包含Vswitch ID',
            }
        """
        request = CreateSnatEntryRequest.CreateSnatEntryRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result
