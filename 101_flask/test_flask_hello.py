#!/usr/bin/env python

import flask_hello
import unittest
import httplib2

class TestFlashHello(unittest.TestCase):

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

    def test_route_with_string(self):
        "=== variable rule string"
        username = "skywalker"
        target_url = self.host_url + '/user/%s' % username
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '200')
        self.assertEqual(body, "User %s" % username)

    def test_route_with_float(self):
        "=== variable rule float"
        test_matrix = {"0.99": "99.0%",
                       "0.999": "99.9%",
                       "0.9999": "99.99%",
                       "0.991234": "99.12%"}
        for case in test_matrix:
            target_url = self.host_url + "/floating/%s" % case
            header, body = self.handle.request(target_url, 'GET')
            self.assertEqual(header['status'], '200')
            self.assertEqual(body, "%s" % test_matrix[case])

    def test_route_with_path(self):
        "=== variable rule path, accept / but ignore parameters"
        test_matrix = {"1/2/3": "1/2/3",
                       "hello%20world": "hello world",
                       "search?q=query": "search"}
        for case in test_matrix:
            target_url = self.host_url + "/show_path/%s" % case
            header, body = self.handle.request(target_url, 'GET')
            self.assertEqual(header['status'], '200')
            # print case, body
            self.assertEqual(body, "%s" % test_matrix[case])

    def test_redirecction_url(self):
        "=== app.route(/project/) cover both /project and /project/ "
        test_path = ['/projects', '/projects/']
        for i in test_path:
            target_url = self.host_url + i
            header, body = self.handle.request(target_url, 'GET')
            self.assertEqual(header['status'], '200')
            self.assertEqual(header['content-location'],
                             self.host_url + "/projects/")
            self.assertEqual(body, "The project page")

    def test_unique_url(self):
        "=== app.route(/about) cover only /about "
        #  /about return 200
        target_url = self.host_url + "/about"
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '200')
        self.assertEqual(header['content-location'],
                         self.host_url + "/about")
        self.assertEqual(body, "The about page")
        #  /about/ return 404
        target_url = self.host_url + "/about/"
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '404')

    def test_http_method(self):
        "=== app.route(/method, method=GET) handle 200 or 405"
        #  GET, PUT, POST return 200
        target_url = self.host_url + "/method"
        for method in ('GET', 'PUT', 'POST'):
            header, body = self.handle.request(target_url, method)
            self.assertEqual(header['status'], '200')
            self.assertIn(method, body)
        #  DELETE return 405
        for method in ('DELETE', ):
            header, body = self.handle.request(target_url, method)
            self.assertEqual(header['status'], '405')

    def test_rendering_template(self):
        "=== render_template(profile.html, name=id)"
        username = "skywalker"
        target_url = self.host_url + '/profile/%s' % username
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '200')
        self.assertIn("Hello %s!" % username, body)


def _retrieve_function_name_from_by_self():
    import sys
    current_module = sys.modules[__name__]
    import inspect
    candidate = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isfunction(obj) and list(name)[0] != '_':
            candidate.append(name)
    return candidate


if __name__ == '__main__':
    unittest.main(verbosity=3)