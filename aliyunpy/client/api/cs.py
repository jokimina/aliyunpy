import re
import json
import yaml
from kubernetes import client as kclient, config

from aliyunsdkcore.request import RoaRequest
from aliyunsdkcs.request.v20151215 import (
    CreateClusterRequest, DescribeClustersRequest,
    DescribeClusterServicesRequest
)
from .base import BaseAliyunApi
from ...exceptions import AliyunClientException
from ..utils import get_logger, MyJsonEncoder

logger = get_logger(__file__)


class CreateK8sClusterRequest(RoaRequest):
    def __init__(self):
        RoaRequest.__init__(self, 'CS', '2015-12-15', 'CreateK8sCluster')
        self.set_uri_pattern('/clusters')
        self.set_method('POST')


class CreateApplicationRequest(RoaRequest):
    def __init__(self):
        RoaRequest.__init__(self, 'CS', '2015-12-15', 'CreateApplication')
        self.set_uri_pattern('/projects')
        self.set_method('POST')


class GetClusterCerts(RoaRequest):
    def __init__(self, cs_id=None):
        if not cs_id:
            raise AliyunClientException('Need cluster id!')
        RoaRequest.__init__(self, 'CS', '2015-12-15', 'CreateApplication')
        self.set_uri_pattern('/k8s/{}/user_config'.format(cs_id))
        self.set_method('GET')


class AliyunCs(BaseAliyunApi):

    def __init__(self, client=None):
        super().__init__(client=client)
        # k8s client
        self._kclients = {}

    def get_client(self, cs_id=None):
        """
        从阿里云api获取证书, 生成对应api client. for kubernetes
        :param cs_id:
        :return:
        """
        _client = self._kclients.get(cs_id, None)
        if not _client:
            request = GetClusterCerts(cs_id=cs_id)
            c = self.client.do_action(request)
            self._kclients[cs_id] = c
            _config = kclient.Configuration()
            _config.verify_ssl = False
            config.kube_config.KubeConfigLoader(
                config_dict=yaml.load(self._kclients.get(cs_id)['config'], Loader=yaml.FullLoader)) \
                .load_and_set(_config)
            _client = kclient.ApiClient(configuration=_config)
            self._kclients[cs_id] = _client
        return _client

    def list_cluster(self, cs_type='all'):
        """
        获取集群信息
        :param cs_type: 集群类型
                        all: 所有类型   aliyun: swarm模式
                        Kubernetes: 原生k8s  ManagedKubernetes: 托管k8s
        :return: 集群列表
        """
        request = DescribeClustersRequest.DescribeClustersRequest()
        result_list = self.client.do_action(request)
        if cs_type != 'all':
            result_list = [r for r in result_list if r.get('cluster_type', '') == cs_type]
        return result_list

    def get_cluster_name_mapper(self):
        return {_c.get('cluster_id', ''): _c.get('name', '') for _c in self.list_clusters()}

    def list_service(self, cs_id='', cs_type='aliyun', without_acs=True):
        """
        列出所有service或pod信息
        :param cs_id: 集群id
        :param cs_type: 集群类型 aliyun/Kubernetes/ManagedKubernetes
        :param without_acs: 不包含阿里云的系统service, 仅限swarm模式有效
        :return:
        """
        result_list = []
        if cs_type == 'aliyun':
            request = DescribeClusterServicesRequest.DescribeClusterServicesRequest()
            request.set_ClusterId(cs_id)
            result_list = self.client.do_action(request)
            if without_acs:
                if result_list:
                    # docker swarm v3无法正确获取到project的值
                    result_list = [_ for _ in result_list if
                                   not re.match(r'^(acs)', _.get('project', 'acs__v3__'))]
        elif 'Kubernetes' in cs_type:
            _client = self.get_client(cs_id=cs_id)
            ext_api = kclient.ExtensionsV1beta1Api(api_client=_client)
            result = ext_api.list_deployment_for_all_namespaces()
            result_list.extend(json.loads(json.dumps(result.items, cls=MyJsonEncoder)))
        return result_list

    def list_ingress(self, cs_id=''):
        """
        列出所有ingress, k8s only
        :param cs_id: 集群id
        :return:
        """
        _client = self.get_client(cs_id=cs_id)
        ext_api = kclient.ExtensionsV1beta1Api(api_client=_client)
        result = ext_api.list_ingress_for_all_namespaces()
        return json.loads(json.dumps(result.items, cls=MyJsonEncoder))

    def get_projects_by_id(self, cs_id):
        pass

    def create_swarm_cluster(self, **kwargs):
        """
        :params:
          https://help.aliyun.com/document_detail/26054.html?spm=a2c4g.11174283.6.759.4abb7a22fS03SN
        :return: cluster, request, task ID
        """
        request = CreateClusterRequest.CreateClusterRequest()
        for k, v in kwargs.items():
            request.add_body_params(k, v)
        result = self.client.do_action(request)
        return result

    def create_k8s_cluster(self, **kwargs):
        """
        :params:
          https://help.aliyun.com/document_detail/87525.html?spm=a2c4g.11186623.6.795.df9139a5lYR57G
        :return: cluster, request, task ID
        """
        request = CreateK8sClusterRequest.CreateK8sClusterRequest()
        for k, v in kwargs.items():
            request.add_body_params(k, v)
        result = self.client.do_action(request)
        return result

    def create_cs_application(self, **kwargs):
        """
        :return: create status
        """
        request = CreateApplicationRequest()
        for k, v in kwargs.items():
            request.add_body_params(k, v)
        result = self.client.do_action(request)
        return result
