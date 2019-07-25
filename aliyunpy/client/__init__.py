from .base import BaseAliyunClient
from . import api


class AliyunClient(BaseAliyunClient):
    ecs = api.AliyunEcs()
    cs = api.AliyunCs()
    slb = api.AliyunSlb()
    vpc = api.AliyunVpc()
    dns = api.AliyunDns()
    ram = api.AliyunRam()
    bss = api.AliyunBss()
    rds = api.AliyunRds()
    redis = api.AliyunRedis()
    kms = api.AliyunKms()
    ons = api.AliyunOns()
    oss = api.AliyunOss()
    drds = api.AliyunDrds()
    pvtz = api.AliyunDnsPrivateZone()
    waf = api.AliyunWaf()
    log = api.AliyunLog()
