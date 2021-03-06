import os
import json
from flask import render_template, request, jsonify, send_from_directory
from app import app

tiles_base_dir = os.path.join(os.getcwd(),'app', 'static','map_tiles')
tile_sources =  os.listdir(tiles_base_dir)

def getZoom(tile):
    base = os.path.splitext(os.path.basename(tile))[0]
    splits = base.split("-")
    return splits[-3]

def generate_tile_provider(tile_dir):
    def inner(filename):
        zoom = getZoom(filename)
        data_dir = os.path.join(tiles_base_dir, tile_dir, zoom)
        return send_from_directory(data_dir, filename)
    print '/%s/<path:filename>'%(tile_dir)
    app.add_url_rule('/%s/<path:filename>'%(tile_dir), tile_dir, inner)
    return inner

tile_functions = map(generate_tile_provider,tile_sources)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/available_wmts_endpoints')
def available_wmts_servers():
    url_strings = {tile_source:"/%s/%s-{z}-{x}-{y}.png" %(tile_source, tile_source) for tile_source in tile_sources}
    return jsonify(url_strings)

#@app.route('/mapbox-tiles/<path:filename>')
#def mapbox_tiles(filename):
#    tile_dir = "mapbox-tiles"
#    zoom = getZoom(filename)
#    print zoom
#    data_dir = os.path.join(tiles_base_dir, tile_dir, zoom)
#    return send_from_directory(data_dir, filename)