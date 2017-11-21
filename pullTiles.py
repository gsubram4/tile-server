# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 16:51:29 2015

@author: scott.philips
"""
import os
import math
import requests
import numpy as np
import time

from PIL import Image
from io import BytesIO

TOKEN = 'pk.eyJ1IjoicmF2ZW5leWVzIiwiYSI6IkpaNkhwLUkifQ.Rjz1PT66ZZhJYwMljuzQQw'
TILES_NAME = "mapbox-tiles"
TILES_DIR = '/Users/gsa0081/Projects/tile-server/app/static/map_tiles/'
TILES_URL = 'https://api.mapbox.com/v4/mapbox.streets/{}/{}/{}.png?access_token=pk.eyJ1IjoicmF2ZW5leWVzIiwiYSI6IkpaNkhwLUkifQ.Rjz1PT66ZZhJYwMljuzQQw'

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile, ytile

# zooms = [5, 6, 7, 8, 9, 10, 11, 12, 13]
#zooms = [1, 2, 3, 4]
zooms = [13, 14, 15, 16]


if True:
    # Phnom Penh
    # min_lat = 10.7
    # max_lat = 12.4
    # min_lon = 103.6
    # max_lon = 106.2

    # min_lat= -14.7
    # max_lat= 34.7
    # min_lon= 78.0
    # max_lon= 150.5

    # min_lat = 4
    # max_lat = 18
    # min_lon = 92
    # max_lon = 117

    # min_lat = 10
    # max_lat = 13
    # min_lon = 103
    # max_lon = 107

    # min_lat = 11
    # max_lat = 12
    # min_lon = 104
    # max_lon = 106

    #min_lat = -85
    #max_lat = 85
    #min_lon = -180
    #max_lon = 180
    
    # Nairobi
    max_lat = -1.1655
    min_lat = -1.4222
    min_lon = 36.6906
    max_lon = 36.9240

    # Djibouti
    # min_lat = 10.9
    # max_lat = 12.6
    # min_lon = 41.5
    # max_lon = 43.6

    tiles = []
    for zoom in zooms:
        lons = np.arange(min_lon, max_lon, .33 * 360 / (2 ** zoom))
        lats = np.arange(min_lat, max_lat, .33 * 170 / (2 ** zoom))
        print(zoom)

        tileSet = set()
        for lat in lats:
            for lon in lons:
                tileSet.add(deg2num(lat, lon, zoom))

        tiles.append(tileSet)

    a = [len(x) for x in tiles]
    print(a)


if True:
    if not os.path.isdir(TILES_DIR):
        exit("Tiles Dir Must Exist")
    
    if not os.path.isdir(os.path.join(TILES_DIR, TILES_NAME)):
        os.mkdir(os.path.join(TILES_DIR,TILES_NAME))

    for zoom in zooms:
        tileSet = tiles[zooms.index(zoom)]
        for i, tile in enumerate(tileSet):
            url = TILES_URL.format(
                zoom, tile[0], tile[1])
            
            if not os.path.isdir(os.path.join(TILES_DIR, TILES_NAME, zoom)):
                os.makedirs(os.path.join(TILES_DIR, TILES_NAME, zoom))
            
            out_file = os.path.join(TILES_DIR,TILES_NAME, zoom, '{}-{}-{}-{}.png'.format(TILES_NAME,zoom, tile[0], tile[1]))

            if os.path.isfile(out_file):
                print("Skipping {}".format(out_file))
                continue

            # time.sleep(.01*np.abs(np.random.randn(1))[0])
            print('{} ({}/{})'.format(out_file, i + 1, len(tileSet)))
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.save(out_file)
            # testfile.retrieve(url, out_file)
