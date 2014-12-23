#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web
import tornado.ioloop

from refine.app.handlers.healthcheck import HealthcheckHandler
from refine.app.handlers.stream import StreamHandler
from refine.app.utils import kls_import

class PyEsReduceRefineServiceApp(tornado.web.Application):

    def __init__(self, redis, config, log_level):
        self.redis = redis
        self.log_level = log_level
        self.config = config

        handlers = [
            (r'/healthcheck', HealthcheckHandler),
            (r'/stream/(?P<job_key>.+)/?', StreamHandler),
        ]

        self.redis.delete('PyEsReduce::mappers')

        self.load_input_streams()
        self.load_reducers()

        super(PyEsReduceRefineServiceApp, self).__init__(handlers)

    def load_input_streams(self):
        self.input_streams = {}

        for stream_class in self.config.INPUT_STREAMS:
            stream = kls_import(stream_class)
            self.input_streams[stream.job_type] = stream()

    def load_reducers(self):
        self.reducers = {}

        for reducer_class in self.config.REDUCERS:
            reducer = kls_import(reducer_class)
            self.reducers[reducer.job_type] = reducer()


