#!/usr/bin/env python
# -*- coding: utf-8 -*-

ALL_KEYS = 'PyEsReduce::*'

# MAPPER KEYS
MAPPERS_KEY = 'PyEsReduce::mappers'
MAPPER_INPUT_KEY = 'PyEsReduce::jobs::%s::input'
MAPPER_OUTPUT_KEY = 'PyEsReduce::jobs::%s::%s::output'
MAPPER_ERROR_KEY = 'PyEsReduce::jobs::%s::errors'
MAPPER_WORKING_KEY = 'PyEsReduce::jobs::%s::working'
LAST_PING_KEY = 'PyEsReduce::mappers::%s::last-ping'
WORKING_KEY = 'PyEsReduce::mappers::%s::working'

# JOB TYPES KEYS
JOB_TYPES_KEY = 'PyEsReduce::job-types'
JOB_TYPES_ERRORS_KEY = 'PyEsReduce::jobs::*::errors'
JOB_TYPE_KEY = 'PyEsReduce::job-types::%s'
JOB_STATUS_KEY = 'PyEsReduce::job-types::status::%s'

# LAST JOB RESULTS KEYS
JOB_LAST_RESULT = 'PyEsReduce::run::job::%s'

# JOB PORT KEY
JOB_PORT_KEY = 'PyEsReduce::jobs::%s::port'

# STATS KEYS
PROCESSED = 'PyEsReduce::stats::processed'
PROCESSED_SUCCESS = 'PyEsReduce::stats::processed::success'
PROCESSED_FAILED = 'PyEsReduce::stats::processed::fail'

# EDIT FILE KEY
CURRENT_EDIT = 'PyEsReduce::edit:current'
CURRENT_CONTENT = 'PyEsReduce::edit:currentcontent'

# JOB TEST RESULT KEY
CURRENT_RESULT = 'PyEsReduce::test::job::content'
JOB_TEST = 'PyEsReduce::test::job::run'

# ElasticSearch Endpoint setting
ELASTIC_ENDPOINT = 'settings::endpoint'
