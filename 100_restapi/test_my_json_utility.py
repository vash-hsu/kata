#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import sys
import getopt
from my_json_utility import recurse_find_json_by_keyword
from my_json_utility import recurse_print_json


json_googlemap_tokyo_japan = """
{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "Tokyo",
               "short_name" : "Tokyo",
               "types" : [ "colloquial_area", "locality", "political" ]
            },
            {
               "long_name" : "Tokyo",
               "short_name" : "Tokyo",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Japan",
               "short_name" : "JP",
               "types" : [ "country", "political" ]
            }
         ],
         "formatted_address" : "Tokyo, Japan",
         "geometry" : {
            "bounds" : {
               "northeast" : {
                  "lat" : 35.8175167,
                  "lng" : 139.9198565
               },
               "southwest" : {
                  "lat" : 35.5208632,
                  "lng" : 139.5629047
               }
            },
            "location" : {
               "lat" : 35.7090259,
               "lng" : 139.7319925
            },
            "location_type" : "APPROXIMATE",
            "viewport" : {
               "northeast" : {
                  "lat" : 35.8175167,
                  "lng" : 139.9198565
               },
               "southwest" : {
                  "lat" : 35.5208632,
                  "lng" : 139.5629047
               }
            }
         },
         "partial_match" : true,
         "place_id" : "ChIJXSModoWLGGARILWiCfeu2M0",
         "types" : [ "colloquial_area", "locality", "political" ]
      },
      {
         "address_components" : [
            {
               "long_name" : "Tokyo",
               "short_name" : "Tokyo",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "Japan",
               "short_name" : "JP",
               "types" : [ "country", "political" ]
            }
         ],
         "formatted_address" : "Tokyo, Japan",
         "geometry" : {
            "bounds" : {
               "northeast" : {
                  "lat" : 35.8986469,
                  "lng" : 153.9875216
               },
               "southwest" : {
                  "lat" : 24.2242344,
                  "lng" : 138.9427579
               }
            },
            "location" : {
               "lat" : 35.6894875,
               "lng" : 139.6917064
            },
            "location_type" : "APPROXIMATE",
            "viewport" : {
               "northeast" : {
                  "lat" : 35.817813,
                  "lng" : 139.910202
               },
               "southwest" : {
                  "lat" : 35.528873,
                  "lng" : 139.510574
               }
            }
         },
         "partial_match" : true,
         "place_id" : "ChIJ51cu8IcbXWARiRtXIothAS4",
         "types" : [ "administrative_area_level_1", "political" ]
      }
   ],
   "status" : "OK"
}

"""

json_foursquare = """
{
  "meta": {
    "code": 200,
    "requestId": "57e0e7ab498eca100be86885"
  },
  "response": {
    "venues": [
      {
        "id": "4b59bab9f964a520fc9428e3",
        "name": "Sushizanmai (すしざんまい 本店)",
        "contact": {
          "phone": "+81335411117",
          "formattedPhone": "+81 3-3541-1117",
          "twitter": "zanmai_man"
        },
        "location": {
          "address": "築地4-11-9",
          "lat": 35.66591290822084,
          "lng": 139.7706225514412,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.66591290822084,
              "lng": 139.7706225514412
            }
          ],
          "distance": 5935,
          "postalCode": "104-0041",
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "築地4-11-9",
            "Chūō, Tōkyō",
            "104-0041",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 5711,
          "usersCount": 4777,
          "tipCount": 93
        },
        "url": "http://www.kiyomura.co.jp/shops/detail/1",
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "503991a1e4b01034f21ae9c7",
        "name": "Genki Sushi (元気寿司 渋谷店)",
        "contact": {
          "phone": "+81334611281",
          "formattedPhone": "+81 3-3461-1281"
        },
        "location": {
          "address": "宇田川町24-8",
          "crossStreet": "レジャープラザビル 1F",
          "lat": 35.66038423280982,
          "lng": 139.69936651803548,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.66038423280982,
              "lng": 139.69936651803548
            }
          ],
          "distance": 6166,
          "postalCode": "150-0042",
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "宇田川町24-8 (レジャープラザビル 1F)",
            "Shibuya, Tōkyō",
            "150-0042",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 2395,
          "usersCount": 1723,
          "tipCount": 47
        },
        "url": "http://www.genkisushi.co.jp",
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 3,
          "summary": "3 people are here",
          "groups": [
            {
              "type": "others",
              "name": "Other people here",
              "count": 3,
              "items": []
            }
          ]
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "51361a56e4b08edd3258acb0",
        "name": "Sushi Bar Sea Dragon (スシバー シードラゴン)",
        "contact": {},
        "location": {
          "address": "千石4-46-7",
          "lat": 35.728289094343324,
          "lng": 139.74329095529586,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.728289094343324,
              "lng": 139.74329095529586
            }
          ],
          "distance": 2375,
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "千石4-46-7",
            "Bunkyō, Tōkyō",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 13,
          "usersCount": 11,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "4bc6a021d35d9c743116e33a",
        "name": "Heiroku Sushi (平禄寿司 表参道店)",
        "contact": {
          "phone": "+81334983968",
          "formattedPhone": "+81 3-3498-3968"
        },
        "location": {
          "address": "神宮前5-8-5",
          "lat": 35.66692836634541,
          "lng": 139.70826923847198,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.66692836634541,
              "lng": 139.70826923847198
            }
          ],
          "distance": 5153,
          "postalCode": "150-0001",
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "神宮前5-8-5",
            "Shibuya, Tōkyō",
            "150-0001",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 880,
          "usersCount": 768,
          "tipCount": 23
        },
        "url": "http://www.heiroku.jp/store/tokyo/omotesando.html",
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "508a0308e4b0ca23f4de0511",
        "name": "Sushi&Vege Japanese Cuisine Aoki",
        "contact": {
          "phone": "+81362286436",
          "formattedPhone": "+81 3-6228-6436"
        },
        "location": {
          "address": "銀座3-4-16",
          "crossStreet": "銀座サニービル 1F",
          "lat": 35.67274881624718,
          "lng": 139.7658294498416,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.67274881624718,
              "lng": 139.7658294498416
            }
          ],
          "distance": 5066,
          "postalCode": "104-0061",
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "銀座3-4-16 (銀座サニービル 1F)",
            "Chūō, Tōkyō",
            "104-0061",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 86,
          "usersCount": 77,
          "tipCount": 2
        },
        "url": "http://cuisine-aoki.com",
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "51ee0111498e3ef54641fc64",
        "name": "Sushi Dining 旬",
        "contact": {
          "phone": "+81335350004",
          "formattedPhone": "+81 3-3535-0004"
        },
        "location": {
          "address": "京橋1-17-12",
          "lat": 35.67767486955928,
          "lng": 139.77359175682068,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.67767486955928,
              "lng": 139.77359175682068
            }
          ],
          "distance": 5130,
          "cc": "JP",
          "city": "Chūō",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "京橋1-17-12",
            "Chūō, Tōkyō",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d11c941735",
            "name": "Sake Bar",
            "pluralName": "Sake Bars",
            "shortName": "Sake Bar",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/nightlife/sake_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 15,
          "usersCount": 14,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "559163d3498ebc1f4aa5ac44",
        "name": "権八 SUSHI 渋谷",
        "contact": {
          "phone": "+81357843772",
          "formattedPhone": "+81 3-5784-3772"
        },
        "location": {
          "address": "3-6 Ｅ・スペースタワー　14F",
          "crossStreet": "円山町",
          "lat": 35.660456270549446,
          "lng": 139.69858868177803,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.660456270549446,
              "lng": 139.69858868177803
            }
          ],
          "distance": 6193,
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "3-6 Ｅ・スペースタワー　14F (円山町)",
            "Shibuya, Tōkyō",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 19,
          "usersCount": 18,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "51b3f305498ec01495ff18e9",
        "name": "Sushi Nakata (江戸前鮨 なか田)",
        "contact": {
          "phone": "+81335036026",
          "formattedPhone": "+81 3-3503-6026"
        },
        "location": {
          "address": "内幸町1-1-1",
          "crossStreet": "帝国ホテル東京 本館 B1F",
          "lat": 35.672536839476564,
          "lng": 139.7583372955447,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.672536839476564,
              "lng": 139.7583372955447
            }
          ],
          "distance": 4708,
          "postalCode": "100-8558",
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "内幸町1-1-1 (帝国ホテル東京 本館 B1F)",
            "Chiyoda, Tōkyō",
            "100-8558",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d111941735",
            "name": "Japanese Restaurant",
            "pluralName": "Japanese Restaurants",
            "shortName": "Japanese",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/japanese_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 22,
          "usersCount": 21,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "4cee42303b03f04dd30d39dc",
        "name": "OPAQUE SUSHI RESTAURANT & LOUNGE",
        "contact": {
          "phone": "+81352934813",
          "formattedPhone": "+81 3-5293-4813"
        },
        "location": {
          "address": "丸の内2-1-1",
          "crossStreet": "マイプラザ 2F",
          "lat": 35.67953988982984,
          "lng": 139.76164519786835,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.67953988982984,
              "lng": 139.76164519786835
            }
          ],
          "distance": 4238,
          "postalCode": "100-0005",
          "cc": "JP",
          "city": "Chiyoda",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "丸の内2-1-1 (マイプラザ 2F)",
            "Chiyoda, Tōkyō",
            "100-0005",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 117,
          "usersCount": 100,
          "tipCount": 2
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "4c2ef93f66e40f47f42cc18b",
        "name": "Sushi Ten (すし天 西麻布)",
        "contact": {
          "phone": "+81337976776",
          "formattedPhone": "+81 3-3797-6776"
        },
        "location": {
          "address": "西麻布4丁目4-16",
          "crossStreet": "nishiazabuビル 2F",
          "lat": 35.65763187865324,
          "lng": 139.72366408923628,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.65763187865324,
              "lng": 139.72366408923628
            }
          ],
          "distance": 5770,
          "postalCode": "106-0031",
          "cc": "JP",
          "city": "Minato",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "西麻布4丁目4-16 (nishiazabuビル 2F)",
            "Minato, Tōkyō",
            "106-0031",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 156,
          "usersCount": 102,
          "tipCount": 1
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "5256935a11d27db64757f1d2",
        "name": "スシヨシ (SUSHI YOSHI)",
        "contact": {
          "phone": "+81332525415",
          "formattedPhone": "+81 3-3252-5415"
        },
        "location": {
          "address": "鍛冶町2-5-9",
          "crossStreet": "国泰神田ビル 1f",
          "lat": 35.688502596028734,
          "lng": 139.78074169892605,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.688502596028734,
              "lng": 139.78074169892605
            }
          ],
          "distance": 4964,
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "鍛冶町2-5-9 (国泰神田ビル 1f)",
            "Chiyoda, Tōkyō",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d111941735",
            "name": "Japanese Restaurant",
            "pluralName": "Japanese Restaurants",
            "shortName": "Japanese",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/japanese_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 8,
          "usersCount": 7,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "4fa5320ce4b0e7038b178b0f",
        "name": "SUSHI BAR YASUDA",
        "contact": {
          "phone": "+81364470232",
          "formattedPhone": "+81 3-6447-0232"
        },
        "location": {
          "address": "南青山4-2-6",
          "crossStreet": "南青山426 B1F",
          "lat": 35.66609664864425,
          "lng": 139.72046673319227,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.66609664864425,
              "lng": 139.72046673319227
            }
          ],
          "distance": 4891,
          "postalCode": "107-0062",
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "南青山4-2-6 (南青山426 B1F)",
            "Minato, Tōkyō",
            "107-0062",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": true,
        "stats": {
          "checkinsCount": 318,
          "usersCount": 293,
          "tipCount": 19
        },
        "url": "http://www.sushibaryasuda.com",
        "menu": {
          "type": "Menu",
          "label": "Menu",
          "anchor": "View Menu",
          "url": "http://www.sushibaryasuda.com/menu.html",
          "mobileUrl": "http://www.sushibaryasuda.com/menu.html",
          "externalUrl": "http://www.sushibaryasuda.com/menu.html"
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "venuePage": {
          "id": "125080605"
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "56e7f681498e88f76faaa38f",
        "name": "Numazuko Sushi",
        "contact": {},
        "location": {
          "lat": 35.690452,
          "lng": 139.703265,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.690452,
              "lng": 139.703265
            }
          ],
          "distance": 3319,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 52,
          "usersCount": 51,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "571b515a498e92ae02b6322f",
        "name": "SUSHI TOKYO TEN",
        "contact": {
          "phone": "+81362748540",
          "formattedPhone": "+81 3-6274-8540"
        },
        "location": {
          "address": "千駄ヶ谷5-24-55",
          "crossStreet": "NEWoMan 2F",
          "lat": 35.68863777488617,
          "lng": 139.7007966041565,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.68863777488617,
              "lng": 139.7007966041565
            }
          ],
          "distance": 3619,
          "postalCode": "151-0051",
          "cc": "JP",
          "neighborhood": "新宿",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "千駄ヶ谷5-24-55 (NEWoMan 2F)",
            "Shibuya, Tōkyō",
            "151-0051",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 28,
          "usersCount": 24,
          "tipCount": 0
        },
        "url": "http://sushitokyo-ten.com",
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "54a3b511498ea948a3fad140",
        "name": "Sushi Mamire",
        "contact": {},
        "location": {
          "lat": 35.694167324654906,
          "lng": 139.70172003361378,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.694167324654906,
              "lng": 139.70172003361378
            }
          ],
          "distance": 3197,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d111941735",
            "name": "Japanese Restaurant",
            "pluralName": "Japanese Restaurants",
            "shortName": "Japanese",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/japanese_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 47,
          "usersCount": 47,
          "tipCount": 2
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "5538853d498e04e927746421",
        "name": "sushi-iwa",
        "contact": {},
        "location": {
          "lat": 35.67004676478329,
          "lng": 139.76439683291727,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.67004676478329,
              "lng": 139.76439683291727
            }
          ],
          "distance": 5235,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 36,
          "usersCount": 36,
          "tipCount": 1
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "4f1bf886e5e85dca132d42a5",
        "name": "sushi 魚奏",
        "contact": {
          "phone": "+81424660666",
          "formattedPhone": "+81 42-466-0666"
        },
        "location": {
          "address": "富士町4-17-7",
          "crossStreet": "地下1階",
          "lat": 35.729171311778295,
          "lng": 139.56494808197021,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.729171311778295,
              "lng": 139.56494808197021
            }
          ],
          "distance": 15262,
          "postalCode": "202-0014",
          "cc": "JP",
          "city": "Nishi-Tokyo-shi",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "富士町4-17-7 (地下1階)",
            "Nishi-Tokyo-shi, Tōkyō",
            "202-0014",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d111941735",
            "name": "Japanese Restaurant",
            "pluralName": "Japanese Restaurants",
            "shortName": "Japanese",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/japanese_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 2,
          "usersCount": 2,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "57d52919498ec7f2c9141944",
        "name": "Sushi Itadori",
        "contact": {},
        "location": {
          "address": "4-10-5 1F",
          "lat": 35.665657,
          "lng": 139.770471,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.665657,
              "lng": 139.770471
            }
          ],
          "distance": 5950,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "4-10-5 1F",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 2,
          "usersCount": 2,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "56b56c5a498ecd024eb0ceed",
        "name": "Sushi Iwase",
        "contact": {},
        "location": {
          "lat": 35.687926170794434,
          "lng": 139.70204414796643,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.687926170794434,
              "lng": 139.70204414796643
            }
          ],
          "distance": 3584,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 1,
          "usersCount": 1,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "553919dc498e07ead0c34985",
        "name": "Sushi Sora at Mandarin Oriental, Tokyo",
        "contact": {
          "phone": "+81120806823",
          "formattedPhone": "+81 120-806-823",
          "twitter": "mo_hotels",
          "facebook": "217354193111",
          "facebookUsername": "MandarinOriental",
          "facebookName": "Mandarin Oriental Hotel Group"
        },
        "location": {
          "address": "2-1-1 Nihonbashi Muromachi",
          "crossStreet": "Chuo-ku",
          "lat": 35.68685464724401,
          "lng": 139.7729531139726,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.68685464724401,
              "lng": 139.7729531139726
            }
          ],
          "distance": 4450,
          "postalCode": "103-8328",
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "2-1-1 Nihonbashi Muromachi (Chuo-ku)",
            "Tokyo, Tōkyō",
            "103-8328",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": true,
        "stats": {
          "checkinsCount": 19,
          "usersCount": 18,
          "tipCount": 0
        },
        "url": "http://www.mandarinoriental.com",
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "storeId": "",
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [
          {
            "id": "556c917ea7c8a11a36bd4578"
          }
        ],
        "hasPerk": false
      },
      {
        "id": "5512b7b7498e1f1f8ba011ce",
        "name": "富士山 Fujiyama Kaiten Sushi",
        "contact": {},
        "location": {
          "address": "Ueno",
          "lat": 35.71042657475168,
          "lng": 139.7756640248401,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.71042657475168,
              "lng": 139.7756640248401
            }
          ],
          "distance": 3950,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Ueno",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 78,
          "usersCount": 59,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "56f68748498e08ac4decea49",
        "name": "sushi-nova",
        "contact": {},
        "location": {
          "lat": 35.712158712867904,
          "lng": 139.792895927077,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.712158712867904,
              "lng": 139.792895927077
            }
          ],
          "distance": 5516,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 38,
          "usersCount": 37,
          "tipCount": 2
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "565d7afb38faaf3d122d6b9e",
        "name": "ougi sushi",
        "contact": {},
        "location": {
          "lat": 35.690362,
          "lng": 139.702185,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.690362,
              "lng": 139.702185
            }
          ],
          "distance": 3402,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 9,
          "usersCount": 8,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "5643327a498edeae9fc3c801",
        "name": "sushi dokoro uoshin",
        "contact": {},
        "location": {
          "lat": 35.67472,
          "lng": 139.736806,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.67472,
              "lng": 139.736806
            }
          ],
          "distance": 3843,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1ce941735",
            "name": "Seafood Restaurant",
            "pluralName": "Seafood Restaurants",
            "shortName": "Seafood",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/seafood_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 2,
          "usersCount": 2,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "559e41ee498e67ab33f93931",
        "name": "The Sushi",
        "contact": {},
        "location": {
          "lat": 35.666743,
          "lng": 139.749804,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.666743,
              "lng": 139.749804
            }
          ],
          "distance": 4974,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 23,
          "usersCount": 13,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "574c15df498ef19a18f15f3d",
        "name": "かっぱ寿司 SUSHI-NOVA 渋谷店",
        "contact": {},
        "location": {
          "lat": 35.66203,
          "lng": 139.697069,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.66203,
              "lng": 139.697069
            }
          ],
          "distance": 6110,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 37,
          "usersCount": 34,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "570f0a00498e133e3f3ecfcc",
        "name": "SUSHI KISARAGI",
        "contact": {
          "phone": "+81368093216",
          "formattedPhone": "+81 3-6809-3216",
          "facebook": "1157235880954525",
          "facebookUsername": "sushikisaragi",
          "facebookName": "Sushi Kisaragi"
        },
        "location": {
          "address": "Shiba 4-4-4",
          "lat": 35.648416,
          "lng": 139.749609,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.648416,
              "lng": 139.749609
            }
          ],
          "distance": 6932,
          "cc": "JP",
          "city": "Tokyo",
          "state": "Tōkyō",
          "country": "Japan",
          "formattedAddress": [
            "Shiba 4-4-4",
            "Minato, Tōkyō",
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 5,
          "usersCount": 3,
          "tipCount": 2
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "56e52c42498eebccdde258c5",
        "name": "SUSHI SAKE いぶき",
        "contact": {},
        "location": {
          "lat": 35.681927,
          "lng": 139.769568,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.681927,
              "lng": 139.769568
            }
          ],
          "distance": 4543,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1c4941735",
            "name": "Restaurant",
            "pluralName": "Restaurants",
            "shortName": "Restaurant",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/default_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 12,
          "usersCount": 12,
          "tipCount": 0
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "554b64f7498e23b054da24bc",
        "name": "Sakura Sushi",
        "contact": {},
        "location": {
          "lat": 35.6946,
          "lng": 139.700536,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.6946,
              "lng": 139.700536
            }
          ],
          "distance": 3265,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [
          {
            "id": "4bf58dd8d48988d1d2941735",
            "name": "Sushi Restaurant",
            "pluralName": "Sushi Restaurants",
            "shortName": "Sushi",
            "icon": {
              "prefix": "https://ss3.4sqi.net/img/categories_v2/food/sushi_",
              "suffix": ".png"
            },
            "primary": true
          }
        ],
        "verified": false,
        "stats": {
          "checkinsCount": 12,
          "usersCount": 11,
          "tipCount": 1
        },
        "allowMenuUrlEdit": true,
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      },
      {
        "id": "542fa303498e8015a94670e8",
        "name": "Sushi Go-Round",
        "contact": {},
        "location": {
          "lat": 35.69763891783556,
          "lng": 139.7985744107712,
          "labeledLatLngs": [
            {
              "label": "display",
              "lat": 35.69763891783556,
              "lng": 139.7985744107712
            }
          ],
          "distance": 6150,
          "cc": "JP",
          "country": "Japan",
          "formattedAddress": [
            "Japan"
          ]
        },
        "categories": [],
        "verified": false,
        "stats": {
          "checkinsCount": 8,
          "usersCount": 8,
          "tipCount": 0
        },
        "specials": {
          "count": 0,
          "items": []
        },
        "hereNow": {
          "count": 0,
          "summary": "Nobody here",
          "groups": []
        },
        "referralId": "v-1474357163",
        "venueChains": [],
        "hasPerk": false
      }
    ]
  }
}
"""


class ParserTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_googlemap_by_recurse_find_json_by_keyword(self):
        "parse json returned from google map API"
        keyword = "location"
        expected_result = [{'lat': 35.7090259, 'lng': 139.7319925},
                           {'lat': 35.6894875, 'lng': 139.6917064}]
        query_result = recurse_find_json_by_keyword(json_googlemap_tokyo_japan,
                                                    keyword)
        # recurse_print_json(json_googlemap_tokyo_japan)
        self.assertEqual(len(query_result), 2);
        self.assertListEqual(query_result, expected_result)

    def test_foursquare_by_recurse_find_json_by_keyword(self):
        "parse json returned from foursquare API"
        # recurse_print_json(json_foursquare)
        query_result = recurse_find_json_by_keyword(json_foursquare, "code")
        print query_result[0]
        self.assertEqual(len(query_result), 1);
        self.assertEqual(query_result[0], 200)


def print_usage(name):
    print "USAGE:"
    print "to list test cases:\n\t%s -l" % (name)
    print "to execute all test cases:\n\t%s" % (name)


def dump_testcase_list():
    testloader = unittest.TestLoader()
    list_testcases = testloader.getTestCaseNames(LinkListTest)
    total_case_nums = len(list_testcases)
    case_counter = 0
    for i in list_testcases:
        case_counter += 1
        print "%d/%d\t%s" %(case_counter, total_case_nums, i)


if __name__ == "__main__":
    scriptfilename = os.path.split(sys.argv[0])[1]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl")
    except getopt.GetoptError:
        print_usage(scriptfilename)
        sys.exit(-1)
    todo_list_testcase = False
    for opt, arg in opts:
        if opt == '-l':
            todo_list_testcase = True
        elif opt == '-h':
            print_usage(scriptfilename)
            sys.exit(-1)
    if todo_list_testcase:
        dump_testcase_list()
    else:
        testloader = unittest.TestLoader()
        testsuit = testloader.loadTestsFromTestCase(ParserTest)
        testruner = unittest.TextTestRunner(verbosity=2)
        testruner.run(testsuit)
