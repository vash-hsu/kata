#!/usr/bin/env python

import json
import httplib2
import getopt
import sys
import os


from my_json_utility import recurse_find_json_by_keyword
from my_json_utility import recurse_print_json
google_api_key = "SAMPLE_KEY_1234567890abcdefghijklmnopqr"


def get_latitude_longitude(city_name, api_key):
    meta_googlemap = getGeocodeLocation(city_name, api_key)
    status_returned = recurse_find_json_by_keyword(meta_googlemap, 'status')
    if len(status_returned) == 0 or status_returned[0] != "OK":
        recurse_print_json(meta_googlemap)
        print "DM: error on parsing json result for %s" % city_name
        return []
    geo_returned = recurse_find_json_by_keyword(meta_googlemap, 'location')
    geo_dict = geo_returned[0]
    try:
        latitude = geo_dict['lat']
        longitude = geo_dict['lng']
        return [latitude, longitude]
    except (TypeError, ValueError) as err:
        print "ERROR: ", str(err)
    return []


def getGeocodeLocation(inputString, api_key):
    # please move this API key outside of source code
    location_string = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'
           % (location_string, api_key))
    handle = httplib2.Http()
    response, content = handle.request(url, 'GET')
    # print "DM: response header:", str(response)
    result = ""
    if 'status' in response and response['status'] == '200':
        try:
            result = json.loads(content)
        except BaseException as err:
            print "DM: json.loads return exception:\n" + repr(err.message)
            result = ""
    return result


def usage():
    script_name = os.path.split(sys.argv[0])[1]
    print "usage:", "%s -k %s" % (script_name, google_api_key)
    print "\tproviding google API key via command line"


def retrieve_apikey_from_user():
    candidate_key = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hk:", ["key="])
    except getopt.GetoptError:
        usage()
        sys.exit(-2)
    for opt, arg in opts:
        if opt in ('-k', "--key"):
            candidate_key = arg
        elif opt == '-h':
            usage()
            sys.exit(0)
    if candidate_key:
        return candidate_key
    else:
        usage()
        sys.exit(-1)


if __name__ == '__main__':
    api_key = retrieve_apikey_from_user()
    location2query = ["Tohyo, Japan",
                      "Jakarta, lndonesia",
                      "Maputo, Mozambique",
                      "Geneva, Switzerland",
                      "Los Angeles California, USA"]
    city2location = dict()
    # send request, receive response, parse json and collect result
    for city_name in location2query:
        city2location[city_name] = get_latitude_longitude(city_name,
                                                          api_key)
    for city_name in city2location:
        print city_name, city2location[city_name]