from .base import BaseAliyunTestCase


class AliyunClientLogTestCase(BaseAliyunTestCase):

    def test_list_project(self):
        r = self.client.log.list_project()
        print(r)

    def test_list_logstore(self):
        r = self.client.log.list_logstore(project_name='acslog-project-cfb0d65eb7-jlgra')
        print([x for x in r if x != 'config-operation-log' and 'py3' not in x])

    def test_delete_logstore(self):
        project_name = 'acslog-project-cfb0d65eb7-jlgra'
        r = self.client.log.list_logstore(project_name=project_name)
        dlist = [x for x in r if x != 'config-operation-log' and 'py3' not in x]
        for logstore in dlist:
            self.client.log_client.delete_logstore(project_name, logstore).log_print()
