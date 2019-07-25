#-*- coding:utf-8 -*-
from aliyunsdkram.request.v20150501 import ListUsersRequest, \
        CreateUserRequest, CreateLoginProfileRequest, \
        ListAccessKeysRequest
from .base import BaseAliyunApi


class AliyunRam(BaseAliyunApi):
    """
    阿里云RAM访问控制相关API
    """
    def get_users(self):
        """
        :return: 阿里云用户列表
        """
        user_list = []
        request = ListUsersRequest.ListUsersRequest()
        request.set_accept_format('json')
        result = self.client.do_action(request)
        if not result['IsTruncated']:
            return result['Users']['User']
        #
        user_list.extend(result['Users']['User'])
        marker = result['Marker'] if 'Marker' in result.keys()\
                else 'MARKER'
        while result['IsTruncated'] or result['IsTruncated'] == 'true':
            request.set_Marker(marker)
            result = self.client.do_action(request)
            user_list.extend(result['Users']['User'])
            marker = request.get_Marker()
        return user_list

    def get_user_ids(self):
        """
        :return: 用户名及ID字典
        """
        return {user['UserName']:user['UserId'] for user in self.get_users()}

    def get_accesskey_owner(self, key):
        """
        :return: 根据access key查找用户名
        """
        users = self.get_user_ids()
        for username in users.keys():
            request = ListAccessKeysRequest.ListAccessKeysRequest()
            request.set_UserName(username)
            result = self.client.do_action(request)['AccessKeys']['AccessKey']
            for item in result:
                if key == item['AccessKeyId']:
                    return {'UserName': username, 'Status': item['Status']}

    def create_user(self, **kwargs):
        """
        :params: 用户名 显示名 邮箱 手机号码 备注
        """
        request = CreateUserRequest.CreateUserRequest()
        request.set_accept_format('json')
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result

    def create_login_profile(self, **kwargs):
        """
        :params:
            UserName
            Password
            PasswordResetRequired
            MFABindRequired
        """
        request = CreateLoginProfileRequest.CreateLoginProfileRequest()
        request.set_accept_format('json')
        for k, v in kwargs.items():
            request.add_query_param(k, v)
        result = self.client.do_action(request)
        return result
