# -*- coding: utf-8 -*-

from mock import Mock
from unittest2 import TestCase
from opbeat.processors import SanitizePasswordsProcessor, RemovePostDataProcessor, \
  RemoveStackLocalsProcessor


class SantizePasswordsProcessorTest(TestCase):
    def test_stacktrace(self):
        data = {
            'stacktrace': {
                'frames': [
                    {
                        'vars': {
                            'foo': 'bar',
                            'password': 'hello',
                            'the_secret': 'hello',
                            'a_password_here': 'hello',
                        },
                    }
                ]
            }
        }

        proc = SanitizePasswordsProcessor(Mock())
        result = proc.process(data)

        self.assertTrue('stacktrace' in result)
        stack = result['stacktrace']
        self.assertTrue('frames' in stack)
        self.assertEquals(len(stack['frames']), 1)
        frame = stack['frames'][0]
        self.assertTrue('vars' in frame)
        vars = frame['vars']
        self.assertTrue('foo' in vars)
        self.assertEquals(vars['foo'], 'bar')
        self.assertTrue('password' in vars)
        self.assertEquals(vars['password'], proc.MASK)
        self.assertTrue('the_secret' in vars)
        self.assertEquals(vars['the_secret'], proc.MASK)
        self.assertTrue('a_password_here' in vars)
        self.assertEquals(vars['a_password_here'], proc.MASK)

    def test_http(self):
        data = {
            'http': {
                'data': {
                    'foo': 'bar',
                    'password': 'hello',
                    'the_secret': 'hello',
                    'a_password_here': 'hello',
                },
                'env': {
                    'foo': 'bar',
                    'password': 'hello',
                    'the_secret': 'hello',
                    'a_password_here': 'hello',
                },
                'headers': {
                    'foo': 'bar',
                    'password': 'hello',
                    'the_secret': 'hello',
                    'a_password_here': 'hello',
                },
                'cookies': {
                    'foo': 'bar',
                    'password': 'hello',
                    'the_secret': 'hello',
                    'a_password_here': 'hello',
                },
            }
        }

        proc = SanitizePasswordsProcessor(Mock())
        result = proc.process(data)

        self.assertTrue('http' in result)
        http = result['http']
        for n in ('data', 'env', 'headers', 'cookies'):
            self.assertTrue(n in http)
            vars = http[n]
            self.assertTrue('foo' in vars)
            self.assertEquals(vars['foo'], 'bar')
            self.assertTrue('password' in vars)
            self.assertEquals(vars['password'], proc.MASK)
            self.assertTrue('the_secret' in vars)
            self.assertEquals(vars['the_secret'], proc.MASK)
            self.assertTrue('a_password_here' in vars)
            self.assertEquals(vars['a_password_here'], proc.MASK)

    def test_querystring_as_string(self):
        data = {
            'http': {
                'query_string': 'foo=bar&password=hello&the_secret=hello&a_password_here=hello',
            }
        }

        proc = SanitizePasswordsProcessor(Mock())
        result = proc.process(data)

        self.assertTrue('http' in result)
        http = result['http']
        self.assertEquals(http['query_string'], 'foo=bar&password=%(m)s&the_secret=%(m)s&a_password_here=%(m)s' % dict(m=proc.MASK))

    def test_querystring_as_string_with_partials(self):
        data = {
            'http': {
                'query_string': 'foo=bar&password&baz=bar',
            }
        }

        proc = SanitizePasswordsProcessor(Mock())
        result = proc.process(data)

        self.assertTrue('http' in result)
        http = result['http']
        self.assertEquals(http['query_string'], 'foo=bar&password&baz=bar' % dict(m=proc.MASK))

    def test_sanitize_credit_card(self):
        proc = SanitizePasswordsProcessor(Mock())
        result = proc.sanitize('foo', '4242424242424242')
        self.assertEquals(result, proc.MASK)


class RemovePostDataProcessorTest(TestCase):
    def test_does_remove_data(self):
        data = {
            'http': {
                'data': 'foo',
            }
        }

        proc = RemovePostDataProcessor(Mock())
        result = proc.process(data)

        self.assertTrue('http' in result)
        http = result['http']
        self.assertFalse('data' in http)


class RemoveStackLocalsProcessorTest(TestCase):
    def test_does_remove_data(self):
        data = {
            'stacktrace': {
                'frames': [
                    {
                        'vars': {
                            'foo': 'bar',
                            'password': 'hello',
                            'the_secret': 'hello',
                            'a_password_here': 'hello',
                        },
                    }
                ]
            }
        }
        proc = RemoveStackLocalsProcessor(Mock())
        result = proc.process(data)

        self.assertTrue('stacktrace' in result)
        stack = result['stacktrace']
        for frame in stack['frames']:
            self.assertFalse('vars' in frame)
