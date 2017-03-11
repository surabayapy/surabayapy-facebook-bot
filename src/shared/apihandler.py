"""
    surabayapy-facebook-bot
    oleh Christoforus Surjoputro
    ~~~~~~~~~
    Modul ini berfungsi untuk menambah fungsi handler dari wheezy.web.

    :license: MIT, see LICENSE for more details.
"""

from wheezy.http.response import method_not_allowed
from wheezy.http.response import HTTPResponse
from wheezy.web.handlers import BaseHandler

class APIHandler(BaseHandler):

    def __call__(self):
        method = self.request.method
        if method == 'GET':
            return self.get()
        elif method == 'POST':
            return self.post()
        elif method == 'PUT':
            return self.put()
        elif method == 'DELETE':
            return self.delete()
        return method_not_allowed()

    def put(self):
        return method_not_allowed()

    def delete(self):
        return method_not_allowed()

    def status_response(self):
        assert not self.errors
        response = HTTPResponse('application/json; charset=UTF-8', 'UTF-8')
        response.write_bytes('{"status":"OK"}')
        return response

    def error_response(self, status_code=200):
        response = self.json_response({'errors': self.errors})
        response.status_code = status_code
        return response
