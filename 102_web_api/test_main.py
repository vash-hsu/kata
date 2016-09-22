#!/usr/bin/env python

import unittest
import httplib2

import main

import urllib
import json
import demjson

class TestFlashRequest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.host_url = 'http://localhost:5000'
        cls.handle = httplib2.Http()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_index_root(self):
        "=== / should return Welcome"
        target_url = self.host_url + "/"
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '200')
        self.assertIn("Welcome", body)

    def test_http_method_put(self):
        "=== PUT send JSON, and get JSON back"
        target_url = self.host_url + "/api/v1"
        prepared_body = """{"message": "Hello Data"}"""
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "PUT",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        self.assertEqual(body,
                         """{"INPUT":{"message":"Hello Data"},"OP":"PUT","status":"ECHO"}""")

if __name__ == '__main__':
    unittest.main(verbosity=2)
