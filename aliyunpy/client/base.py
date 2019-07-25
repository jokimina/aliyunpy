# pylint: disable=unused-argument
import os
import inspect
import json
import logging
import oss2

from aliyun.log import LogClient
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from . import monkey
from .api.base import BaseAliyunApi
from ..exceptions import AliyunClientException

logger = logging.getLogger(__name__)

monkey.patch_all()


def _is_api_endpoint(obj):
    return isinstance(obj, BaseAliyunApi)


class BaseAliyunClient:

    def __new__(cls, *args, **kwargs):
        self = super(BaseAliyunClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, access_key=None, access_secret=None, region_id='cn-beijing', **kwargs):
        self._acs_client = AcsClient(access_key, access_secret, region_id=region_id, **kwargs)
        self._log_client = LogClient(
            os.environ.get('ALIYUN_LOG_SAMPLE_ENDPOINT', 'cn-beijing.log.aliyuncs.com'),
            access_key, access_secret
        )
        self._oss_auth = oss2.Auth(access_key, access_secret)

    def _decode_result(self, res):
        try:
            result = json.loads(res, strict=False)
        except (TypeError, ValueError):
            return res
        return result

    def do_action(self, request):
        try:
            res = self._acs_client.do_action_with_exception(request)
        except (ClientException, ServerException) as e:
            raise AliyunClientException(e.error_code, e.message)
        result = self._decode_result(res)

        if isinstance(result, (dict, list)):
            return result
        raise AliyunClientException(-1, "Can not decode response as JSON\n{}".format(result))

    @property
    def acs_client(self):
        return self._acs_client

    @property
    def oss_auth(self):
        return self._oss_auth

    @property
    def log_client(self):
        return self._log_client
