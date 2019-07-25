# pylint: disable=all
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.http import format_type
from aliyunsdkcore.http.http_response import HttpResponse


def patch_all():
    AcsClient._make_http_response = _make_http_response


def _make_http_response(self, endpoint, request, timeout, specific_signer=None):
    body_params = request.get_body_params()
    if body_params:
        body = json.dumps(body_params)
        request.set_content(body)
        request.set_content_type(format_type.APPLICATION_JSON)
    elif request.get_content() and "Content-Type" not in request.get_headers():
        request.set_content_type(format_type.APPLICATION_OCTET_STREAM)
    method = request.get_method()

    signer = self._signer if specific_signer is None else specific_signer
    header, url = signer.sign(self._region_id, request)

    if self.get_user_agent() is not None:
        header['User-Agent'] = self.get_user_agent()
    if header is None:
        header = {}
    header['x-sdk-client'] = 'python/2.0.0'

    protocol = request.get_protocol_type()
    response = HttpResponse(
        endpoint,
        url,
        method,
        header,
        protocol,
        request.get_content(),
        self._port,
        timeout=timeout)
    if body_params:
        body = json.dumps(body_params)
        response.set_content(body, "utf-8", format_type.APPLICATION_JSON)
    return response
