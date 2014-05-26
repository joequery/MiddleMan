###############################
# Middle man Flask app base
###############################
from flask import Flask, request, render_template, jsonify
from pyparsing import ParseException

import datetime
import json
import requests

from mmlib.jsonparser import apply_scheme_to_json
from mmlib.flaskhelpers.forms import extract_post_data
from mmlib.flaskhelpers.json_traversal import codify_json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/json_extract', methods=['GET'])
def json_extract():
    return render_template("json_extract.html")

@app.route('/test_traversal', methods=['GET'])
def test_traversal():
    return render_template("test_traversal.html")

@app.route('/test_codify_json', methods=['GET'])
def test_codify_json():
    rawJSON = """
{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "1600",
               "short_name" : "1600",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "Amphitheatre Pkwy",
               "short_name" : "Amphitheatre Pkwy",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Mountain View",
               "short_name" : "Mountain View",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Santa Clara",
               "short_name" : "Santa Clara",
               "types" : [ "administrative_area_level_2", "political" ]
            },
            {
               "long_name" : "California",
               "short_name" : "CA",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "United States",
               "short_name" : "US",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "94043",
               "short_name" : "94043",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
         "geometry" : {
            "location" : {
               "lat" : 37.42291810,
               "lng" : -122.08542120
            },
            "location_type" : "ROOFTOP",
            "viewport" : {
               "northeast" : {
                  "lat" : 37.42426708029149,
                  "lng" : -122.0840722197085
               },
               "southwest" : {
                  "lat" : 37.42156911970850,
                  "lng" : -122.0867701802915
               }
            }
         },
         "types" : [ "street_address" ]
      }
   ],
   "status" : "OK"
}
"""
    codified_json = codify_json(rawJSON)
    return render_template("codify_json.html", codified_json=codified_json)

@app.route('/process', methods=['POST'])
def process():
    required_fields = ('scheme', 'url')
    post,errors = extract_post_data(request, required_fields)

    if errors:
        return jsonify(errors=errors)

    r = requests.get(post['url'])

    if r.status_code != 200:
        err_msg = 'Request to %s did not return 200.' % post['url']
        return err_msg

    try:
        data = json.loads(r.content)
        rawjson = json.dumps(data) # formatting
    except ValueError:
        return "Invalid JSON"

    try:
        result = apply_scheme_to_json(post['scheme'], rawjson)
    except ParseException, e:
        return e.msg

    return result

@app.route('/sampledata', methods=['GET'])
def sample_data():
    url="https://api.forecast.io/forecast/18b4aae350b6ce1e1940e715e4a317f4/30.3389,-97.7707"

    scheme=render_template("examplescheme.html")

    return jsonify(url=url, scheme=scheme)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
