#!/usr/bin/env python

import json
import httplib2
import getopt
import sys
import os
from datetime import datetime
from my_json_utility import recurse_find_json_by_keyword
from my_json_utility import recurse_print_json


CLIENT_ID = "SAMPLE_ID_FOR_FOURSQUARE_0123456789ABCDEFGHIJKLM"
CLIENT_SECRET = "SAMPLE_SECRET_FOR_FOURSQUARE_0123456789ABCDEFGHI"

# https://api.foursquare.com/v2/venues/search
#   ?client_id=CLIENT_ID
#   &client_secret=CLIENT_SECRET
#   &v=20130815
#   &ll=40.7,-74
#   &query=sushi


def get_datetime_string():
    """
    :return: "20160920"
    """
    return datetime.now().strftime("%Y%m%d")


def get_restaurant(location, meal_type,
                   client_id=CLIENT_ID,
                   client_secret=CLIENT_SECRET):
    """
    :param location: string
    :param meal_type: string
    :param client_id: string
    :param client_secret: string
    :return: empty list or list of json type (dictionary)
    """
    # [40.7, -71] -> "40.7,-74"
    str_location = '%s,%s' % (str(location[0]), str(location[1]))
    query_url = 'https://api.foursquare.com/v2/venues/search?' + \
        'client_id=%s' % client_id + \
        '&client_secret=%s' % client_secret + \
        '&v=%s' % get_datetime_string() + \
        '&ll=%s' % str_location + \
        '&query=%s' % meal_type
    # print "DM: query_url =", query_url
    handle = httplib2.Http()
    response, content = handle.request(query_url, "GET")
    if 'status' not in response or response['status'] != '200':
        return list()
    #
    result_code = recurse_find_json_by_keyword(content, 'code')
    if len(result_code) == 0 or result_code[0] != 200:
        return list()
    #
    restaurants = recurse_find_json_by_keyword(content, 'venues')
    return restaurants


def usage():
    script_name = os.path.split(sys.argv[0])[1]
    print "usage:", "%s --id %s --sec %s" %\
                    (script_name, CLIENT_ID, CLIENT_SECRET)
    print "\tproviding foursquare cline ID and Secret"


def retrieve_id_and_secret_from_user():
    """
    :return: [client_id, client_secret]
    """
    client_id = ""
    client_secret = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:s:", ["id=", "sec="])
    except getopt.GetoptError:
        usage()
        sys.exit(-2)
    for opt, arg in opts:
        if opt in ('-i', "--id"):
            client_id = arg
        if opt in ('-s', "--sec"):
            client_secret = arg
        elif opt == '-h':
            usage()
            sys.exit(0)
    return [client_id, client_secret]


def get_first_one_restaurant(meal_type, location,
                             client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET):
    the_one = None
    restaurants = get_restaurant(location, meal_type,
                                 client_id, client_secret)
    if restaurants and restaurants[0] and isinstance(restaurants[0], list):
        the_one = restaurants[0][0]
    return the_one


def get_photo_url_by_id(id,
                        client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET):
    url = "https://api.foursquare.com/v2/venues/%s/photos?" % id + \
          "client_id=%s&v=%s&client_secret=%s" % (client_id,
                                                  get_datetime_string(),
                                                  client_secret)
    handle = httplib2.Http()
    header, response = handle.request(url, "GET")
    json_dict = json.loads(response)
    if json_dict['response']['photos']['items']:
        first_pic = json_dict['response']['photos']['items'][0]
        prefix = first_pic['prefix']
        suffix = first_pic['suffix']
        url_image = prefix + "300x300" + suffix
    else:
        url_image = ""
    return url_image


if __name__ == '__main__':
    location2query = [35.7090259, 139.7319925]
    # the_one = get_first_one_restaurant("Sushi", location2query)
    client_id, client_secret = retrieve_id_and_secret_from_user()
    if len(client_id) == 0 or len(client_secret) == 0:
        usage()
        sys.exit(-1)
    the_one = get_first_one_restaurant("Sushi", location2query,
                                       client_id, client_secret)
    recurse_print_json(the_one)
    #
    url = get_photo_url_by_id(the_one['id'], client_id, client_secret)
    print url

