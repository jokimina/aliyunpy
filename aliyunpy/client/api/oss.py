import oss2
from .base import BaseAliyunApi


class AliyunOss(BaseAliyunApi):
    default_endpoint = 'http://oss-cn-beijing.aliyuncs.com'

    def list_bucket(self):
        """
        列出当前所有oss bucket
        https://help.aliyun.com/document_detail/31957.html?spm=a2c4g.11186623.6.1105.4c9e556cYuWTBJ
        :return:
        """
        result_list = []
        service = oss2.Service(self.client.oss_auth, self.default_endpoint)
        result = service.list_buckets()
        buckets = result.buckets
        result_list.extend(buckets)
        if result.is_truncated:
            r = service.list_buckets(marker=result.next_marker)
            result_list.extend(r.buckets)
            while True:
                if r.is_truncated:
                    r = service.list_buckets(marker=result.next_marker)
                    result_list.extend(r.buckets)
                break
        result_list = [r.__dict__ for r in result_list]
        return result_list
