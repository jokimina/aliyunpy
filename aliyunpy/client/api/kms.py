from aliyunsdkkms.request.v20160120 import DecryptRequest, EncryptRequest
from .base import BaseAliyunApi


class AliyunKms(BaseAliyunApi):
    def decrypt_blob(self, cipher_blob):
        request = DecryptRequest.DecryptRequest()
        request.set_CiphertextBlob(cipher_blob)
        result = self.client.do_action(request)
        return result.get('Plaintext')

    def encrypt_blob(self, key_id, plain_blob):
        request = EncryptRequest.EncryptRequest()
        request.set_KeyId(key_id)
        request.set_Plaintext(plain_blob)
        result = self.client.do_action(request)
        return result.get('CiphertextBlob')
