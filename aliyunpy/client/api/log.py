from .base import BaseAliyunApi


class AliyunLog(BaseAliyunApi):
    """
    阿里云日志服务
    https://github.com/aliyun/aliyun-log-python-sdk/blob/master/tests/sample.py
    """
    def list_project(self):
        return self.client.log_client.list_project(size=-1).get_projects()

    def list_logstore(self, project_name=None, logstore_name_pattern=None):
        return self.client.log_client.list_logstore(project_name=project_name,
                                                    logstore_name_pattern=logstore_name_pattern, size=-1).get_logstores()

    def delete_logstore(self, project_name, logstore):
        return self.client.log_client.delete_logstore(project_name, logstore)
