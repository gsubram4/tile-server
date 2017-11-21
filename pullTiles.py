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
TILES_DIR = '/Users/caa0107/Documents/projects/SABI/src/foreshadow/mapstr/app/static/map_tiles/tiles'

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return xtile, ytile

# zooms = [5, 6, 7, 8, 9, 10, 11, 12, 13]
zooms = [1, 2, 3, 4]
# zooms = [13, 14]

# # Bounding boxes expressed as [min_lon, max_lon, min_lat, max_lat]
# bbox_phnom_penh = [103.6, 106.2, 10.7, 12.4]
# bbox_djibouti = [41.5, 43.6, 10.9, 12.6]
#
# BOUNDING_BOXES = {
#     'phnom_penh': bbox_phnom_penh,
#     'djibouti': bbox_djibouti
# }
#
# def get_tile_sets(bbox, min_zoom, max_zoom):
#
#     min_lon = bbox[0]
#     max_lon = bbox[1]
#     min_lat = bbox[2]
#     max_lat = bbox[3]
#
#     tiles = []
#     for zoom in range(min_zoom, max_zoom + 1):
#         print('Building tile requests for zoom {}'.format(zoom))
#         lons = np.arange(min_lon, max_lon, .33 * 360 / (2 ** zoom))
#         lats = np.arange(min_lat, max_lat, .33 * 170 / (2 ** zoom))
#
#         tile_set = set()
#         for lat in lats:
#             for lon in lons:
#                 tile_set.add(deg2num(lat, lon, zoom))
#
#         tiles.append(tile_set)
#
#     return tiles
#
#
#
# def get_tiles(roi, min_zoom, max_zoom):
#     bbox = BOUNDING_BOXES[roi]
#
#     tile_sets = get_tile_sets(bbox, min_zoom, max_zoom)
#
#     for tile_set in tile_sets:
#         for tile in tile_set:
#             out_file = os.path.join('tiles_phnom_penh', 'mapbox-tiles-{}-{}-{}.png'.format(zoom, tile[0], tile[1]))
#             url = 'https://api.mapbox.com/v4/mapbox.streets/{}/{}/{}.png?access_token={}'.format(
#                 zoom, tile[0], tile[1], TOKEN)


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

    min_lat = -85
    max_lat = 85
    min_lon = -180
    max_lon = 180

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
        os.mkdir(TILES_DIR)

    for zoom in zooms:
        tileSet = tiles[zooms.index(zoom)]
        for i, tile in enumerate(tileSet):
            url = 'https://api.mapbox.com/v4/mapbox.streets/{}/{}/{}.png?access_token={}'.format(
                zoom, tile[0], tile[1], TOKEN)

            out_file = os.path.join(TILES_DIR, 'mapbox-tiles-{}-{}-{}.png'.format(zoom, tile[0], tile[1]))

            # if os.path.isfile(out_file):
            #     print("Skipping {}".format(out_file))
            #     continue

            # time.sleep(.01*np.abs(np.random.randn(1))[0])
            print('{} ({}/{})'.format(out_file, i + 1, len(tileSet)))
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.save(out_file)
            # testfile.retrieve(url, out_file)


# if False:
#     filesPath = '/Users/scott.philips/Documents/SABI/STROfflineDemo/static/tiles'
#     files = [f for f in os.listdir(filesPath) if '.png' in f]
#
#     for f in files:
#         fsplit = f.split('-')
#         zoom = fsplit[2]
#         x = fsplit[3]
#         y = fsplit[4].split('.')[0]
#
#         testfile = urllib.URLopener()
#         url =  'https://b.tiles.mapbox.com/v3/examples.map-cnkhv76j/%s/%s/%s@2x.png'%(zoom,x,y)
#         out_file = "mapbox-darktiles-%s-%s-%s.png"%(zoom,x,y)
#         if os.path.isfile(out_file):
#             print "Skipping"
#             continue
#         time.sleep(.5*np.abs(np.random.randn(1))[0])
#         print out_file
#         testfile.retrieve(url,out_file)
