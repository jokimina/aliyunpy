class AliyunException(Exception):
    def __init__(self, errcode=None, errmsg=None):
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return 'Error code: {0}, message: {1}'.format(self.errcode, self.errmsg)

    def __repr__(self):
        return '{cls}({code}, {msg})'.format(cls=self.__class__.__name__,\
            code=self.errcode, msg=self.errmsg)


class AliyunClientException(AliyunException):
    pass
