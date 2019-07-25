# -*- coding:utf-8 -*-
from aliyunsdkalidns.request.v20150109 import DescribeDomainsRequest, \
    DescribeDomainRecordsRequest
from .base import BaseAliyunApi


class AliyunDns(BaseAliyunApi):
    """
    阿里云DNS相关API
    """

    def get_dns_list(self):
        """
        获取DNS列表
        :return: DNS列表
        """
        request = DescribeDomainsRequest.DescribeDomainsRequest()
        request.set_accept_format('json')
        request.set_PageNumber(1)
        request.set_PageSize(100)

        first_page_result = self.client.do_action(request)
        total_count, page_size = first_page_result['TotalCount'], \
                                 first_page_result['PageSize']

        if total_count <= page_size:
            return first_page_result['Domains']['Domain']
        result_list = first_page_result['Domains']['Domain']
        _page_num = (total_count / page_size) \
            if total_count % page_size == 0 \
            else (int(total_count / page_size) + 1)
        for _page in range(2, _page_num + 1):
            request.set_PageNumber(_page)
            page_result = self.client.do_action(request)
            result_list.extend(page_result['Domains']['Domain'])
        return result_list

    def get_record_count(self, domain_name):
        """
        :return: 对应域名解析记录总数
        """
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(domain_name)
        record_count = self.client.do_action(request)['TotalCount']
        return record_count

    def get_dns_record(self, domain_name):
        """
        获取DNS解析记录
        :params: 二级域名
        :return: 对应域名解析记录
        """
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_PageNumber(1)
        request.set_PageSize(100)
        request.set_DomainName(domain_name)

        first_page_result = self.client.do_action(request)
        total_count, page_size = first_page_result['TotalCount'], \
                                 first_page_result['PageSize']

        if total_count <= page_size:
            return first_page_result['DomainRecords']['Record']
        result_list = first_page_result['DomainRecords']['Record']
        _page_num = (total_count / page_size) \
            if total_count % page_size == 0 \
            else (int(total_count / page_size) + 1)
        for _page in range(2, _page_num + 1):
            request.set_PageNumber(_page)
            page_result = self.client.do_action(request)
            result_list.extend(page_result['DomainRecords']['Record'])
        return result_list
