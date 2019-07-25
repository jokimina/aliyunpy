import json
import httpretty
from .base import BaseAliyunTestCase
from .config import auto_load_fixture, suppress_warnings


class AliyunClientCsTestCase(BaseAliyunTestCase):

    @suppress_warnings
    @httpretty.activate
    @auto_load_fixture
    def test_list_cluster(self):
        self.assertEqual(3, len(self.client.cs.list_cluster()))
        self.assertEqual('aliyun', self.client.cs.list_cluster(cs_type='aliyun')[0].get('cluster_type'))
        self.assertEqual('Kubernetes', self.client.cs.list_cluster(cs_type='Kubernetes')[0].get('cluster_type'))
        self.assertEqual('ManagedKubernetes', self.client.cs.list_cluster(cs_type='ManagedKubernetes')[0]
                         .get('cluster_type'))

    def test_list_cluster_real(self):
        r = self.client.cs.list_cluster()
        # r = [x['cluster_type'] for x in r]
        print(json.dumps(r, indent=2, ensure_ascii=False))

    @suppress_warnings
    def test_list_service(self):
        r = self.client.cs.list_service(cs_id='c3f555f50caf14faeb0b380eb3621e09f')
        # r = self.client.cs.list_service(cs_id='c9001581cfd71416a88e3d69534439052', cs_type='Kubernetes')
        # d = list(set([x['project'] for x in r]))
        d = list(set([s["project"] for s in r]))
        print("\n".join(d))
        # d = r[0]
        # d.sort()
        # print(f'Total count: {len(d)}')
        # print('\n'.join(d))
        # d = r[0]
        # print(json.dumps(d, indent=2, ensure_ascii=False))
        # print(d.get('metadata', {}).get('labels', {}).get('app', ''))

    def test_list_ingress(self):
        r = self.client.cs.list_ingress(cs_id='c9001581cfd71416a88e3d69534439052')
        d = r[0]
        print(json.dumps(d, indent=2, ensure_ascii=False))
