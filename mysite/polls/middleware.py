import logging
import time


from django.http.request import HttpRequest

import oneagent

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class DynatraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        oneagent.logger = logger

        if not oneagent.initialize():
            logger.error('Error initialiing OneAgent SDK')

        else:
            self.sdk = oneagent.get_sdk()

            self.wappinfo = self.sdk.create_web_application_info(
                virtual_host='example.com',
                application_id='DjangoApp',
                context_root='/')

    def __call__(self, request: HttpRequest):
        with self.sdk.trace_incoming_web_request(self.wappinfo,
                                                 request.get_raw_uri(),
                                                 request.method,
                                                 headers=request.headers):

            response = self.get_response(request)

        return response
