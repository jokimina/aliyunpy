import time
from aliyunsdkons.request.v20190214 import (
    OnsRegionListRequest, OnsInstanceInServiceListRequest,
    OnsTopicListRequest
)
from .base import BaseAliyunApi


class AliyunOns(BaseAliyunApi):
    def get_regions(self, id_only=False):
        """
        获取支持的region列表
        https://help.aliyun.com/document_detail/29622.html?spm=a2c4g.11186623.6.594.66a64614BsQKrj
        :param id_only: 是否只返回region id列表
        :return:
        """
        request = OnsRegionListRequest.OnsRegionListRequest()
        request.set_PreventCache(int(time.time()))
        result = self.client.do_action(request)
        result_list = result.get('Data', {}).get('RegionDo', [])
        if id_only:
            result_list = list(set([x.get('OnsRegionId') for x in result_list]))
        return result_list

    def get_instances(self):
        """
        获取实例列表, 返回所有region
        https://help.aliyun.com/document_detail/106351.html?spm=a2c4g.11186623.6.599.22155c8c7rg3Wk

        {
          "Data": {
            "InstanceVO": [
              {
                "InstanceStatus": 5,
                "IndependentNaming": false,
                "InstanceId": "MQ_INST_1726708279589269_C54T0Yxx",
                "InstanceName": "DEFAULT_INSTANCE",
                "InstanceType": 1
              }
            ]
          },
          "HelpUrl": "",
          "RequestId": "CCD70385-9445-42F1-959E-A4EC62756DE5"
        }
        :return:
        {
          "cn-beijing": [
            {
              "InstanceStatus": 5,
              "IndependentNaming": false,
              "InstanceId": "MQ_INST_1726708279589269_C54T0Yxx",
              "InstanceName": "DEFAULT_INSTANCE",
              "InstanceType": 1
            }
          ]
        }
        """
        result_dict = {}
        request = OnsInstanceInServiceListRequest.OnsInstanceInServiceListRequest()
        request.set_PreventCache(int(time.time()))
        regions = self.get_regions(id_only=True)
        for region in regions:
            self.client.acs_client.set_region_id(region)
            result = self.client.do_action(request)
            instance_list = result.get('Data', {}).get('InstanceVO', [])
            if instance_list:
                result_dict[region] = instance_list
        return result_dict

    def list_topic(self, region='mq-internet-access', instance_id=None):
        """
        查询账号下所有 Topic 的信息列表
        https://help.aliyun.com/document_detail/29590.html?spm=a2c4g.11174283.6.604.31de449cQdtRnc
        :param instance_id: ons 实例id
        :param region: region id
        :return:
         [{
            "Relation": 1,
            "Owner": "1726708279589269",
            "RelationName": "所有者",
            "IndependentNaming": false,
            "InstanceId": "MQ_INST_1726708279589269_yyyyy8Ak",
            "CreateTime": 1446036003000,
            "Topic": "TeleSpiderTest",
            "Remark": "",
            "MessageType": 0
          }
        ]
        """
        request = OnsTopicListRequest.OnsTopicListRequest()
        request.set_PreventCache(int(time.time()))
        request.set_InstanceId(instance_id)
        self.client.acs_client.set_region_id(region)
        result = self.client.do_action(request)
        topics = result.get('Data', {}).get('PublishInfoDo', [])
        return topics

    def list_topic_all(self):
        """
        获取所有region和instance下的topic
        :return:
        [{
          "RegionId": "ap-southeast-1",
          "Relation": 1,
          "Owner": "1726708279589269",
          "RelationName": "所有者",
          "IndependentNaming": false,
          "InstanceId": "MQ_INST_1726708279589269_yyyyy6d0",
          "CreateTime": 1546401123000,
          "Topic": "MarsEventTaskSingapore",
          "Remark": "新加坡集群风控结果通知",
          "MessageType": 0
        }]
        """
        result_list = []
        instance_dict = self.get_instances()
        for region, instances in instance_dict.items():
            for instance in instances:
                topics = self.list_topic(region=region,
                                         instance_id=instance.get('InstanceId'))
                for topic in topics:
                    result_list.append(dict(RegionId=region, **topic))
        return result_list
