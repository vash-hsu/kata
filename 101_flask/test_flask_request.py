#!/usr/bin/env python

import flask_hello
import unittest
import httplib2
import urllib

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
        "=== / should return index page"
        target_url = self.host_url + "/"
        header, body = self.handle.request(target_url, 'GET')
        # print "DM: header=", header
        # print "DM: body=", body
        self.assertEqual(header['status'], '200')
        self.assertEqual(body, "index page")

    def test_hello(self):
        "=== /hello should return Hello World!"
        target_url = self.host_url + "/hello"
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '200')
        self.assertEqual(body, "Hello World!")

    def test_http_method(self):
        "=== GET return 200 , PUT/POST return 3-1, DELETE return 405"
        #  GET, PUT, POST return 200
        target_url = self.host_url + "/method"
        for method in ('GET',):
            header, body = self.handle.request(target_url, method)
            self.assertEqual(header['status'], '200')
            self.assertIn(method, body)
        for method in ('PUT', 'POST'):
            header, body = self.handle.request(target_url, method)
            self.assertEqual(header['status'], '301')
            self.assertIn(method, body)
        #  DELETE return 405
        for method in ('DELETE', ):
            header, body = self.handle.request(target_url, method)
            self.assertEqual(header['status'], '405')

    def test_login_with_post_form(self):
        "POST, request.form[username] and request.form[password]"
        # GET, 200 return
        target_url = self.host_url + "/login"
        header, body = self.handle.request(target_url, "GET")
        self.assertEqual(header['status'], '200')
        # POST
        request_header = {'Content-type': 'application/x-www-form-urlencoded'}
        post_data = {'username': 'admin', 'password': 'admin'}
        request_body = urllib.urlencode(post_data)
        # print "DM: request_body =", request_body
        header, body = \
            self.handle.request(target_url, "POST",
                                body=request_body,
                                headers=request_header)
        self.assertEqual(header['status'], '301')
        self.assertIn('admin', body)
        # POST with failing login
        post_data = {'username': 'admin', 'password': 'wrong'}
        request_body = urllib.urlencode(post_data)
        header, body = self.handle.request(target_url, "POST",
                                           body=request_body,
                                           headers=request_header)
        self.assertEqual(header['status'], '200')
        self.assertNotIn('admin', body)

    def test_login_with_parameter(self):
        "POST by /login/root?password=root"
        # GET, 200 return
        target_url = self.host_url + "/login/root?password=root"
        header, body = self.handle.request(target_url, "GET")
        self.assertEqual(header['status'], '200')
        self.assertNotIn('root', body)
        # POST
        header, body = self.handle.request(target_url, "POST")
        self.assertEqual(header['status'], '301')
        self.assertIn('root', body)
        # fail to login
        target_url = self.host_url + "/login/root?password=wrong"
        header, body = self.handle.request(target_url, "POST")
        self.assertEqual(header['status'], '200')
        self.assertNotIn('root', body)

if __name__ == '__main__':
    unittest.main(verbosity=2)
