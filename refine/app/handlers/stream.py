#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
from uuid import uuid4
from ujson import dumps, loads
from datetime import datetime

import tornado.web
import tornado.gen

from refine.app.handlers import BaseHandler
from refine.app.utils import DATETIME_FORMAT
from refine.app.keys import PROCESSED, PROCESSED_FAILED, PROCESSED_SUCCESS, JOB_STATUS_KEY, JOB_TYPE_KEY, MAPPER_INPUT_KEY, MAPPER_OUTPUT_KEY, MAPPER_ERROR_KEY, JOB_LAST_RESULT

class StreamHandler(BaseHandler):
    def group_items(self, stream_items, group_size):
        items = []
        current_item = []
        items.append(current_item)
        for stream_item in stream_items:
            if len(current_item) == group_size:
                current_item = []
                items.append(current_item)
            current_item.append(stream_item)
        return items

    @tornado.web.asynchronous
    def get(self, job_key):
        getLast = self.get_argument("last", default="0", strip=False)
        if (self.redis.exists(JOB_LAST_RESULT % job_key) and getLast == "1"):
            result = self.redis.get(JOB_LAST_RESULT % job_key)
            self.set_header('Content-Type', 'application/json')
            self.write(result)
            self.finish()
        else:
            arguments = self.request.arguments
            job_id = uuid4()
            job_date = datetime.now()

            job_type_input_queue = JOB_TYPE_KEY % job_key
            self.redis.sadd(job_type_input_queue, str(job_id))
            job_status = JOB_STATUS_KEY % job_key
            try:
                start = time.time()
                self.redis.set(job_status, "STREAMING")
                input_stream = self.application.input_streams[job_key]
                items = input_stream.process(self.application, arguments)
                logging.warning("before group, total item size is %d" %(len(items)))
                if hasattr(input_stream, 'group_size'):
                    items = self.group_items(items, input_stream.group_size)
                logging.warning("after group, total item size is %d" %(len(items)))
                mapper_input_queue = MAPPER_INPUT_KEY % job_key
                mapper_output_queue = MAPPER_OUTPUT_KEY % (job_key, job_id)
                mapper_error_queue = MAPPER_ERROR_KEY % job_key
                with self.redis.pipeline() as pipe:
                    start = time.time()

                    for item in items:
                        msg = {
                            'output_queue': mapper_output_queue,
                            'job_id': str(job_id),
                            'job_key': job_key,
                            'item': item,
                            'date': job_date.strftime(DATETIME_FORMAT),
                            'retries': 0
                        }
                        pipe.rpush(mapper_input_queue, dumps(msg))
                    pipe.execute()
                logging.warning("input queue took %.2f" % (time.time() - start))
                self.redis.set(job_status, "MAPPING")
                start = time.time()
                results = []
                errored = False
                retry = 3
                while (len(results) < len(items)):
                #    logging.warning("During mapping, items size %d, results size %d" %(len(items), len(results)))
                    output = self.redis.blpop(mapper_output_queue, timeout=5)
                    if output:
                        retry = 3
                        key, item = output
                        json_item = loads(item)
                        if 'error' in json_item:
                            logging.warning("error occurred in mapping")
                            json_item['retries'] -= 1
                            self.redis.hset(mapper_error_queue, json_item['job_id'], dumps(json_item))
                            errored = True
                            break
                        oldresults = len(results)
                        results.append(loads(json_item['result']))
                        newresults = len(results)
                    else:
                        retry = retry - 1
                        if retry <= 0:
                            logging.warning("error occurred in mapping, mapper has long time no return")
                            self.redis.delete(mapper_input_queue)
                            break
                self.redis.delete(mapper_output_queue)
                logging.warning("map took %.2f" % (time.time() - start))
                if errored:
                    self.redis.incr(PROCESSED)
                    self.redis.incr(PROCESSED_FAILED)
                    self.redis.set(job_status, "ERROR")
                    self.redis.set(JOB_LAST_RESULT % job_key, "ERROR")
                    self._error(500, 'Mapping failed. Check the error queue.')
                else:
                    start = time.time()
                    self.redis.set(job_status, "REDUCING")
                    reducer = self.application.reducers[job_key]
                    result = reducer.reduce(self.application, results)
                    logging.warning("reduce took %.2f" % (time.time() - start))

                    self.set_header('Content-Type', 'application/json')

                    self.redis.set(JOB_LAST_RESULT % job_key, dumps(result))
                    self.write(dumps(result))

                    self.redis.incr(PROCESSED)
                    self.redis.incr(PROCESSED_SUCCESS)

                    self.finish()
                    self.redis.set(job_status, "IDLE")
            finally:
                self.redis.srem(job_type_input_queue, str(job_id))

