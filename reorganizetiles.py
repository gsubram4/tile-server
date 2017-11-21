
from glob import glob
import os
from tqdm import tqdm

TILES_DIR = '/Users/gsa0081/Projects/tile-server/app/static/map_tiles/mapbox-tiles'

allTiles = glob("%s/*.png" % (TILES_DIR))

def getZoom(tile):
    base = os.path.splitext(os.path.basename(tile))[0]    
    splits = base.split("-")
    return splits[-3]

allZooms = set(map(getZoom, allTiles))

for zoom in allZooms:
    if not os.path.isdir("%s/%s" % (TILES_DIR, zoom)):
        os.makedirs("%s/%s" % (TILES_DIR, zoom))
   
for tile in tqdm(allTiles):
    zoom = getZoom(tile)
    base = os.path.basename(tile)
    os.rename(tile, "%s/%s/%s" % (TILES_DIR, zoom, base))     