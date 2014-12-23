#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os


import logging
import argparse

import tornado.ioloop
from tornado.httpserver import HTTPServer
import redis

from refine.app.app import PyEsReduceRefineServiceApp
from refine.app.config import Config


def main(arguments=None):
    '''Runs PyEsReduce Refine server with the specified arguments.'''

    parser = argparse.ArgumentParser(description='runs the application that processes stream requests for PyEsReduce')
    parser.add_argument('-b', '--bind', type=str, default='0.0.0.0', help='the ip that PyEsReduce will bind to')
    parser.add_argument('-p', '--port', type=int, default=9999, help='the port that PyEsReduce will bind to')
    parser.add_argument('-l', '--loglevel', type=str, default='warning', help='the log level that PyEsReduce will run under')
    parser.add_argument('--redis-host', type=str, default='0.0.0.0', help='the ip that PyEsReduce will use to connect to redis')
    parser.add_argument('--redis-port', type=int, default=6379, help='the port that PyEsReduce will use to connect to redis')
    parser.add_argument('--redis-db', type=int, default=0, help='the database that PyEsReduce will use to connect to redis')
    parser.add_argument('--redis-pass', type=str, default='', help='the password that PyEsReduce will use to connect to redis')
    parser.add_argument('-c', '--config-file', type=str, help='the config file that PyEsReduce will use to load input stream classes and reducers', required=True)

    args = parser.parse_args(arguments)

    cfg = Config(args.config_file)

    c = redis.StrictRedis(host=args.redis_host, port=args.redis_port, db=args.redis_db, password=args.redis_pass)

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    application = PyEsReduceRefineServiceApp(redis=c, config=cfg, log_level=args.loglevel.upper())

    server = HTTPServer(application)
    server.bind(args.port, args.bind)
    server.start(1)

    try:
        logging.debug('PyEsReduce Refine service app running at %s:%d' % (args.bind, args.port))
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print
        print "-- PyEsReduce Refine service app closed by user interruption --"

if __name__ == "__main__":
    main(sys.argv[1:])
