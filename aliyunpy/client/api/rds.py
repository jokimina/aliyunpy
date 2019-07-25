import random
import string
import time

from aliyunsdkrds.request.v20140815 import CreateDBInstanceRequest, \
    CreateDatabaseRequest, DescribeRegionsRequest, \
    CreateAccountRequest, GrantAccountPrivilegeRequest, \
    DescribeDBInstancesRequest
from .base import BaseAliyunApi


class AliyunRds(BaseAliyunApi):
    """
    Aliyun RDS related API
    """

    def get_regions(self, id_only=False):
        """
        获取支持的region列表
        https://help.aliyun.com/document_detail/26243.html
        :param id_only: 是否只返回region id列表
        :return:
        """
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        result = self.client.do_action(request)
        result_list = result.get('Regions', {}).get('RDSRegion', [])
        if id_only:
            result_list = list(set([x.get('RegionId') for x in result_list]))
        return result_list

    def list_rds(self, name_only=False, **kwargs):
        """
        获取实例列表
        https://help.aliyun.com/document_detail/26232.html?spm=a2c4g.11186623.6.1322.16ff69b2We0YoY
        :param name_only: 是否只返回name列表
        :param kwargs:
        :return:
        """
        result_list = []
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        regions = self.get_regions(id_only=True)
        for region in regions:
            request.set_PageSize(100)
            request.set_PageNumber(1)
            for k, v in kwargs.items():
                request.add_query_param(k, v)
            request.add_query_param('RegionId', region)
            result = self.client.do_action(request)
            result_list.extend(result.get('Items', {}).get('DBInstance', []))

            total_count = float(result.get('TotalCount', 0))
            if not total_count:
                continue
            page_count = float(result.get('PageSize', 1))
            _p = total_count / page_count
            if _p > 1:
                for _p_num in range(2, int(_p) + 2):
                    # 防止限流
                    time.sleep(1)
                    request.set_PageNumber(_p_num)
                    result = self.client.do_action(request)
                    result_list.extend(result.get('Items', {}).get('DBInstance', []))

        if name_only:
            result_list = [i['InstanceName'] for i in result_list]
        return result_list

    def create_rds(self, **kwargs):
        request = CreateDBInstanceRequest.CreateDBInstanceRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_rds_mini(self, **kwargs):
        """
        RDS最小化配置
        """
        params = {
            'Engine': 'MySQL',
            'EngineVersion': '5.6',
            'DBInstanceClass': 'rds.mysql.s2.large',
            'DBInstanceStorage': 100,
            'DBInstanceNetType': 'Intranet',
            'DBInstanceStorageType': 'local_ssd',
            'SystemDBCharset': 'utf8',
            'InstanceNetworkType': 'VPC',
            # 'VPCId': 'VPC ID',
            # 'VSwitchId': 'Vswitch ID',
            'PayType': 'Prepaid',
            'UsedTime': 1,
            'Period': 'Month',
        }
        kwargs.update(params)
        result = self.create_rds(**kwargs)
        return result

    def create_rds_database(self, **kwargs):
        request = CreateDatabaseRequest.CreateDatabaseRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_rds_databases(self, instance_id, db_list, charset='utf8'):
        results = []
        if not isinstance(db_list, list):
            raise TypeError
        for db in db_list:
            result = self.create_rds_database(
                DBInstanceId=instance_id,
                DBName=db,
                CharacterSetName=charset,
            )
            results.append(result)
        return results

    def create_rds_account(self, **kwargs):
        request = CreateAccountRequest.CreateAccountRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def grant_account_privi(self, **kwargs):
        request = GrantAccountPrivilegeRequest.GrantAccountPrivilegeRequest()
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_database_apollo(self, instance_id):
        account = 'apollo'
        db_list = ['configserverprod', 'portalserver']
        _password_base = string.ascii_letters + \
                         string.digits + \
                         '!@#$%^&'
        _password_length = 16
        _password = ''.join([random.choice(_password_base) for _ in \
                             range(_password_length)])
        # Create databases
        db_result = self.create_rds_databases(
            instance_id,
            db_list,
            charset='utf8',
        )
        if not db_result:
            raise Exception("Create Apollo databases failed.")
        # Create apollo account
        account_result = self.create_rds_account(
            DBInstanceId=instance_id,
            AccountName=account,
            AccountPassword=_password,
            AccountDescription='Apollo account',
        )
        if not account_result:
            raise Exception("Create Apollo account failed.")
        # Grant privileges to apollo
        for db in db_list:
            grant_result = self.grant_account_privi(
                DBInstanceId=instance_id,
                AccountName=account,
                DBName=db,
                AccountPrivilege='ReadWrite',
            )
            if not grant_result:
                raise Exception("Grant to apollo failed.")
        return {'Account': 'apollo', 'Password': _password}
