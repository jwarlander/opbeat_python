# -*- coding: utf-8 -*-

import datetime
import uuid
from unittest2 import TestCase

from opbeat.utils import opbeat_json as json


class JSONTest(TestCase):
    def test_uuid(self):
        res = uuid.uuid4()
        self.assertEquals(json.dumps(res), '"%s"' % res.hex)

    def test_datetime(self):
        res = datetime.datetime(day=1, month=1, year=2011, hour=1, minute=1, second=1)
        self.assertEquals(json.dumps(res), '"2011-01-01T01:01:01.000000Z"')

    def test_set(self):
        res = set(['foo', 'bar'])
        self.assertEquals(json.dumps(res), '["foo", "bar"]')

    def test_frozenset(self):
        res = frozenset(['foo', 'bar'])
        self.assertEquals(json.dumps(res), '["foo", "bar"]')
