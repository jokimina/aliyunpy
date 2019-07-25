import json
import logging
import datetime


def get_logger(name=None):
    return logging.getLogger('aliyunpy.%s' % name)


def date_to_isoformat_datetime(d, timedelta=8):
    return (d - datetime.timedelta(hours=timedelta)).isoformat(timespec='seconds') + 'Z'


def isoformat_to_datetime(s, timedelta=8, strp='%Y-%m-%dT%H:%M:%SZ'):
    return datetime.datetime.strptime(s, strp) + datetime.timedelta(hours=timedelta)


class MyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__dict__'):
            return {k.lstrip('_'): v for k, v in o.__dict__.items()}
        else:
            return o.__str__()
