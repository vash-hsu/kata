#!/usr/bin/env python

import unittest
import httplib2

import main

import urllib
import json
import demjson

class TestFlaskRequest(unittest.TestCase):

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

    def test_api_split_version_resource(self):
        "input v1/resource, return [v1, resource]"
        target_path = "v1/resource"
        results = main._api_split_version_resource(target_path)
        self.assertEqual(results, ['v1', 'resource'])
        target_path = "v1/resource/123456789"
        results = main._api_split_version_resource(target_path)
        self.assertEqual(results, ['v1', 'resource', '123456789'])

    def test_api_v1_api_get_all_elements_list(self):
        "=== GET and then get JSON back"
        target_url = self.host_url + "/api/v1/resource"
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '200')
        self.assertEqual(header['content-type'], "application/json")
        json_dict = demjson.decode(body)
        self.assertGreater(int(json_dict["status"]), 0)

    def test_api_v1_api_get_element_by_id(self):
        "=== GET and then get JSON back"
        target_url = self.host_url + "/api/v1/resource/123456789"
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '200')
        self.assertEqual(header['content-type'], "application/json")
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict["status"], '1')
        self.assertIn("golden key", json_dict["value"])

    def test_api_v1_api_get_element_by_not_found_id(self):
        "=== GET  with undefined resource_id, and then get JSON back with status 0"
        target_url = self.host_url + "/api/v1/resource/notdefined"
        header, body = self.handle.request(target_url, 'GET')
        self.assertEqual(header['status'], '200')
        self.assertEqual(header['content-type'], "application/json")
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict["status"], '0')

    def test_api_v1_put_by_existent_id(self):
        "=== PUT /api/v1/resource/golden_data and get status=1 in jason back"
        target_url = self.host_url + "/api/v1/resource/test_data"
        prepared_body = demjson.encode({'new_element': 'new data'})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "PUT",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict['status'], '1')
        self.assertEqual(json_dict['id'], 'test_data')

    def test_api_v1_put_disallow_nonexistent_id(self):
        "=== PUT /api/v1/resource/undefined and get status=-1 " \
        "to indicate not allow to update non-existent resouroce-id"
        target_url = self.host_url + "/api/v1/resource/undefined"
        prepared_body = demjson.encode({'new_element': 'new data'})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "PUT",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertLess(json_dict['status'], '0')
        # print "DM: json_dict =", repr(json_dict)

    def test_api_v1_post_by_creating_new_id_without_slash(self):
        "=== POST /api/v1/resource and get status=1 after inserting new resource_id"
        target_url = self.host_url + "/api/v1/resource"
        prepared_body = demjson.encode({'ending_without_slash': 'dummy data'})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "POST",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict['status'], '1', 'ending without slash')
        self.assertEqual(len(json_dict['id']), 40) # in form of sha1 string

    def test_api_v1_post_by_creating_new_id_with_slash(self):
        "=== POST /api/v1/resource/ and get status=1 after inserting new resource_id"
        target_url = self.host_url + "/api/v1/resource/"
        prepared_body = demjson.encode({'ending_with_slash': 'dummy data'})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "POST",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict['status'], '1', 'ending with slash')
        self.assertEqual(len(json_dict['id']), 40) # in form of sha1 string

    def test_api_v1_post_then_delete(self):
        "=== POST /api/v1/resource/ and get resource_id back, then DELETE it"
        target_url = self.host_url + "/api/v1/resource"
        prepared_body = demjson.encode({'ha ha': 'create and then delete'})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "POST",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict['status'], '1')
        working_resource_id = json_dict['id']
        # then delete it
        target_url = self.host_url + "/api/v1/resource" + \
                     "/" + working_resource_id
        prepared_body = demjson.encode({})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "DELETE",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict['status'], '1')
        self.assertEqual(json_dict['id'],
                         working_resource_id,
                         "kill the wrong guy?")

    def test_api_v1_delete_disallow_nonexistent_id(self):
        "=== DELETE /api/v1/resource/undefined and get status=-1 " \
        "to indicate not allow to delete non-existent resouroce-id"
        target_url = self.host_url + "/api/v1/resource/undefined"
        prepared_body = demjson.encode({})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "DELETE",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict['status'], '-1')
        print "DM:", repr(json_dict)

    def test_api_v1_delete_disallow_action_without_id(self):
        "=== DELETE /api/v1/resource and get status=-1 "
        target_url = self.host_url + "/api/v1/resource"
        prepared_body = demjson.encode({})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "DELETE",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict['status'], '-1')
        # with slash
        target_url = self.host_url + "/api/v1/resource/"
        prepared_body = demjson.encode({})
        prepared_header = {'Content-Type': 'application/json'}
        header, body = self.handle.request(target_url, "DELETE",
                                           body=prepared_body,
                                           headers=prepared_header)
        self.assertEqual(header['status'], '200')
        json_dict = demjson.decode(body)
        self.assertEqual(json_dict['status'], '-1')

if __name__ == '__main__':
    unittest.main(verbosity=2)
