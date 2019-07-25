from .. import base  # pylint: disable=unuse-import


class BaseAliyunApi:
    """ Aliyun base class"""

    def __init__(self, client=None):
        self.client = client  # type: base.BaseAliyunClient
