#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web

from refine.app.utils import logger

class BaseHandler(tornado.web.RequestHandler):
    def _error(self, status, msg=None):
        self.set_status(status)
        if msg is not None:
            logger.error(msg)
        self.finish()

    @property
    def redis(self):
        return self.application.redis


