import os
import sys
import re
import inspect
import json
from functools import wraps
import httpretty



def read_fixture(function):
    path = os.path.join(os.path.dirname(inspect.getfile(function)) + os.sep + 'fixtures',
                        function.__name__.lstrip('test_') + '.json')
    with open(path, 'rb') as f:
        return f.read()


def auto_set_fixture(path=None, is_json=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not path:
                fixture = read_fixture(func)
            else:
                with open(path, 'rb') as f:
                    fixture = f.read()
            if is_json:
                fixture = json.loads(fixture)
            kwargs.update({'fixture': fixture})
            return func(*args, **kwargs)

        return wrapper

    return decorator


def auto_load_fixture(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        httpretty.register_uri(httpretty.GET, re.compile(r'^.*\.aliyuncs\.com.*$'), body=read_fixture(func),
                               content_type='application/json')
        return func(*args, **kwargs)

    return wrapper


def suppress_warnings(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)

    return wrapper
