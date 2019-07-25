[![Python3](https://img.shields.io/badge/python-3.7-green.svg?style=plastic)](https://www.python.org/) 
## 阿里云SDK, 官方的觉得有点难用所以简单封装了下, 内部用起来比较顺手, 不过比较粗糙, 有人用的话会考虑好好完善下.
### 使用示例
```python
from aliyunpy.client import AliyunClient
c = AliyunClient('xxx', 'xxx', 'cn-beijing')
c.ecs.get_ecs_all()
```

### 上传到私有pypiserver
#### 本地pipyserver配置
```bash
$ cat ~/.pypirc
[distutils]
index-servers = sample

[sample]
repository: http://pypi.sample.com/
username: sample
password: xxxx
```
#### 上传 
```bash
python setup.py sdist upload -r sample
```

### 参考
- 项目结构参考: [wechatpy](https://github.com/jxtech/wechatpy)