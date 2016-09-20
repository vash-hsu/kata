#!/usr/bin/env python


from gmap_helper import get_latitude_longitude
from foursquare_helper import get_first_one_restaurant
from foursquare_helper import get_photo_url_by_id
from my_json_utility import recurse_find_json_by_keyword
from my_json_utility import recurse_print_json

import json
import httplib2
import getopt
import os
import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

googlemap_api_key = "SAMPLE_KEY_1234567890abcdefghijklmnopqr"
foursquare_client_id = "SAMPLE_ID_FOR_FOURSQUARE_0123456789ABCDEFGHIJKLM"
foursquare_client_secret = "SAMPLE_SECRET_FOR_FOURSQUARE_0123456789ABCDEFGHI"


def findARestaurant(mealType, location):
    geography = []
    #1. Use getGeocodeLocation to get the latitude and longitude
    #  coordinates of the location string.
    geography = get_latitude_longitude(location, googlemap_api_key)
    # print "DM:", geography
    #2. Use foursquare API to find a nearby restaurant
    # with the latitude, longitude, and mealType strings.
    # 3. Grab the first restaurant
    the_one = get_first_one_restaurant(mealType, geography,
                                       client_id=foursquare_client_id,
                                       client_secret=foursquare_client_secret)
    #4. Get a  300x300 picture of the restaurant using the venue_id
    # (you can change this by altering the 300x300 value in the URL
    # or replacing it with 'orginal' to get the original picture
    # print "DM: the_one =", the_one
    id = the_one['id']
    name = the_one['name']
    address = ' '.join(the_one['location']['formattedAddress'])
    # 5. Grab the first image
    photo_url = get_photo_url_by_id(id,
                                    client_id=foursquare_client_id,
                                    client_secret=foursquare_client_secret)
    #6. If no image is available, insert default a image url
    # ?
    #7. Return a dictionary containing the restaurant name, address, and image url
    dict_restaurant = {'name': name, 'address': address, 'image': photo_url}
    print "Restaurant Name: %s" %  dict_restaurant['name']
    print "Restaurant Address: %s" % dict_restaurant['address']
    print "Image: %s" % dict_restaurant['image']
    print


def retrieve_credentials_from_user():
    """
    :return: [api_key, client_id, client_secret]
    """
    api_key = ""
    client_id = ""
    client_secret = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hk:i:s:",
                                   ["key=", "id=", "sec="])
    except getopt.GetoptError:
        usage()
        sys.exit(-2)
    for opt, arg in opts:
        if opt in ('-k', "--key"):
            api_key = arg
        elif opt in ('-i', "--id"):
            client_id = arg
        elif opt in ('-s', "--sec"):
            client_secret = arg
        elif opt == '-h':
            usage()
            sys.exit(0)
    return [api_key, client_id, client_secret]


def usage():
    script_name = os.path.split(sys.argv[0])[1]
    print "usage:", "%s --key %s --id %s --sec %s" %\
                    (script_name,
                     googlemap_api_key,
                     foursquare_client_id,
                     foursquare_client_secret)
    print "\tproviding google map API key, foursquare cline ID and Secret"


if __name__ == '__main__':
    _key, _id, _secret = retrieve_credentials_from_user()
    if len(_key) ==0 or len(_id) == 0 or len(_secret) == 0:
        usage()
        sys.exit(-1)
    googlemap_api_key = _key
    foursquare_client_id = _id
    foursquare_client_secret = _secret
    #
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
