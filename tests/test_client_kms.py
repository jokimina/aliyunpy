from .base import BaseAliyunTestCase


class AliyunClientKmsTestCase(BaseAliyunTestCase):

    def test_encrypt_blob(self):
        key_id = '5a4f1d32-8d22-4afe-bddd-5915aa3ade27'
        cipher = self.client.kms.encrypt_blob(key_id, 'xx')
        self.assertEqual(len(cipher), 152)

    def test_decrypt_blob(self):
        cipher_blob = 'MWVhMzdjNjQtYzUzNi00M2I0LWE4ZjYtOTNmYzk1NWYxZjNhRlpBNXR1Z2YxK0Jva2ZHMEdZSmZhRHBndW9tdjBNd1ZBQUFBQUFBQUFBQXV2SkNvYWVEZVBmNyswQXpSNyt2NUlNYjFjV3pNVUpVPQ=='
        plain = self.client.kms.decrypt_blob(cipher_blob)
        self.assertEqual(plain, 'xx')
