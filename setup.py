from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(name='aliyunpy',
      version='1.0.0',
      author='jokimina',
      author_email='jokimina@163.com',
      description='aliyun sdk tools',
      install_requires=requirements,
      packages=find_packages()
)
