# -*- coding: utf-8 -*-
# use Baidu geocoder services by get

# 2019.02.22  MXY
# + get_geocoder
# + load_json

import requests
import json
import re

ak = "dVXsnvuHuAavjDjxrDGNAAnN216s0F2r"
# ak = 'tQG6hv6020b7ljc2slLuVixua8Me2glp'

baidu_url = "http://api.map.baidu.com/geocoder/v2/?"


# get geocoder by get
# params can reference to 'http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding-abroad'
# example:
#   http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location=35.658651,139.745415&output=json&pois=1&ak=您的ak
# important input:
#   location: <lat>, <lng>
#   output: "json" or "xml"
#
def get_geocoder(
        location=None,
        coordtype="bd09II",
        ret_coordtype="bd09II",
        pois=0,
        radius=1000,
        ak=ak,
        sn=None,
        output='xml',
        callback=None,
        extensions_poi=None,
        extensions_road=False,
        extensions_town=None,
        language='zh-CN',
        language_auto=1,
        latest_admin=1,
):
    # # for test
    # url = 'http://api.map.baidu.com/geocoder/v2/?location= 35.658651,139.745415&output=json&pois=1&ak=' + ak

    if extensions_road is False:
        extensions_road = 'false'
    else:
        extensions_road = 'true'
    if extensions_town is False:
        extensions_town = 'false'
    else:
        extensions_town = 'true'

    url = baidu_url \
          + 'location=' + location \
          + '&coordtype=' + coordtype \
          + '&ret_coordtype=' + ret_coordtype \
          + '&pois=' + str(pois) \
          + '&radius=' + str(radius) \
          + '&ak=' + ak \
          + '&sn=' + str(sn) \
          + '&output=' + output \
          + '&callback=' + str(callback) \
          + '&extensions_poi=' + str(extensions_poi) \
          + '&extensions_road=' + str(extensions_road) \
          + '&extensions_town=' + str(extensions_town) \
          + '&language=' + language \
          + '&language_auto=' + str(language_auto) \
          + '&latest_admin=' + str(latest_admin)
    req = requests.get(url)
    # req = req.read()
    # print(req)
    # print(type(req.text))
    return req.text
    # pass


# extract json from get_geocoder
# input:
#   req_txt: the result from get_geocoder
def load_json(req_txt):
    # but req_txt is not pure json text
    # it need to remove something
    # like: None&&None( json )
    req_txt = re.sub('^None&&None\(', '', req_txt)
    req_txt = re.sub('\)$', '', req_txt)
    # load json
    req = json.loads(req_txt)
    return req['result']['formatted_address'], \
           req['result']['addressComponent']['direction'], \
           req['result']['addressComponent']['distance']
    # pass


# get two functions together
# input:
#   location
def main(location):
    address_return = {}
    req_txt = get_geocoder(
        location=location,
        pois=1,
        radius=300,
        output='json'
    )
    address, direction, distance = load_json(req_txt)
    if distance is '':
        pass
    else:
        distance = str(distance) + 'm'
    address_return['address'] = address
    address_return['direction'] = direction
    address_return['distance'] = distance
    return address_return


if __name__ == '__main__':
    # req_txt = get_geocoder(
    #     location='32.048994,118.772351',
    #     pois=1,
    #     radius=300,
    #     output='json'
    # )
    # address, direction, distance = load_json(req_txt)
    # print(address)
    # print(direction)
    # print(distance)
    address_return = main('32.048994,118.772351')
    print(address_return)



