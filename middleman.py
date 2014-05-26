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
  "hourly": {
    "icon": "partly-cloudy-day", 
    "data": [
      {
        "ozone": 309.53, 
        "temperature": 71.62, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 67.26, 
        "humidity": 0.86, 
        "visibility": 9.82, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 71.62, 
        "pressure": 1016.25, 
        "windSpeed": 7.4, 
        "cloudCover": 0.76, 
        "time": 1400652000, 
        "windBearing": 161, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 309.67, 
        "temperature": 70.71, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 66.48, 
        "humidity": 0.87, 
        "visibility": 9.43, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 70.71, 
        "pressure": 1016.25, 
        "windSpeed": 11.73, 
        "cloudCover": 0.8, 
        "time": 1400655600, 
        "windBearing": 165, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 309.69, 
        "temperature": 70.43, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 66.18, 
        "humidity": 0.86, 
        "visibility": 9.38, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 70.43, 
        "pressure": 1016.2, 
        "windSpeed": 12.91, 
        "cloudCover": 0.86, 
        "time": 1400659200, 
        "windBearing": 168, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 309.63, 
        "temperature": 70.43, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.93, 
        "humidity": 0.86, 
        "visibility": 9.37, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 70.43, 
        "pressure": 1016.22, 
        "windSpeed": 13.47, 
        "cloudCover": 0.89, 
        "time": 1400662800, 
        "windBearing": 169, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 309.47, 
        "temperature": 70.17, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.55, 
        "humidity": 0.85, 
        "visibility": 9.46, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 70.17, 
        "pressure": 1016.34, 
        "windSpeed": 13.26, 
        "cloudCover": 0.89, 
        "time": 1400666400, 
        "windBearing": 171, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 309.22, 
        "temperature": 69.81, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.51, 
        "humidity": 0.86, 
        "visibility": 9.5, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 69.81, 
        "pressure": 1016.53, 
        "windSpeed": 11.58, 
        "cloudCover": 0.87, 
        "time": 1400670000, 
        "windBearing": 171, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 308.98, 
        "temperature": 69.85, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 65.53, 
        "humidity": 0.86, 
        "visibility": 9.43, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 69.85, 
        "pressure": 1016.81, 
        "windSpeed": 11.27, 
        "cloudCover": 0.84, 
        "time": 1400673600, 
        "windBearing": 171, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 308.85, 
        "temperature": 71.1, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 65.7, 
        "humidity": 0.83, 
        "visibility": 9.55, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 71.1, 
        "pressure": 1017.32, 
        "windSpeed": 12.1, 
        "cloudCover": 0.81, 
        "time": 1400677200, 
        "windBearing": 171, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 308.72, 
        "temperature": 73.03, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 65.42, 
        "humidity": 0.77, 
        "visibility": 9.9, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 73.03, 
        "pressure": 1018.01, 
        "windSpeed": 13.47, 
        "cloudCover": 0.76, 
        "time": 1400680800, 
        "windBearing": 172, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 308.3, 
        "temperature": 75.42, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 65.76, 
        "humidity": 0.72, 
        "visibility": 9.99, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 75.42, 
        "pressure": 1018.39, 
        "windSpeed": 14.52, 
        "cloudCover": 0.72, 
        "time": 1400684400, 
        "windBearing": 172, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 307.29, 
        "temperature": 78.3, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 65.93, 
        "humidity": 0.66, 
        "visibility": 10, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 78.3, 
        "pressure": 1018.26, 
        "windSpeed": 14.6, 
        "cloudCover": 0.66, 
        "time": 1400688000, 
        "windBearing": 171, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 306, 
        "temperature": 81.19, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 65.59, 
        "humidity": 0.59, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 83.19, 
        "pressure": 1017.81, 
        "windSpeed": 14.62, 
        "cloudCover": 0.56, 
        "time": 1400691600, 
        "windBearing": 168, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 305, 
        "temperature": 83.74, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 64.98, 
        "humidity": 0.53, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 85.52, 
        "pressure": 1017.3, 
        "windSpeed": 14.9, 
        "cloudCover": 0.55, 
        "time": 1400695200, 
        "windBearing": 165, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.62, 
        "temperature": 85.79, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 64.26, 
        "humidity": 0.49, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 87.25, 
        "pressure": 1016.73, 
        "windSpeed": 15.3, 
        "cloudCover": 0.41, 
        "time": 1400698800, 
        "windBearing": 161, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.53, 
        "temperature": 87.16, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 63.64, 
        "humidity": 0.46, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 88.34, 
        "pressure": 1016.1, 
        "windSpeed": 15.98, 
        "cloudCover": 0.36, 
        "time": 1400702400, 
        "windBearing": 156, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.36, 
        "temperature": 87.88, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 62.86, 
        "humidity": 0.43, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 88.71, 
        "pressure": 1015.59, 
        "windSpeed": 16.36, 
        "cloudCover": 0.34, 
        "time": 1400706000, 
        "windBearing": 151, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.89, 
        "temperature": 87.73, 
        "icon": "clear-day", 
        "dewPoint": 62.17, 
        "humidity": 0.43, 
        "visibility": 10, 
        "summary": "Clear", 
        "apparentTemperature": 88.25, 
        "pressure": 1015.24, 
        "windSpeed": 16.8, 
        "cloudCover": 0.22, 
        "time": 1400709600, 
        "windBearing": 149, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.34, 
        "temperature": 86.68, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 62.05, 
        "humidity": 0.44, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 87.18, 
        "pressure": 1015.05, 
        "windSpeed": 16.91, 
        "cloudCover": 0.3, 
        "time": 1400713200, 
        "windBearing": 146, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 302.98, 
        "temperature": 85.07, 
        "icon": "clear-day", 
        "dewPoint": 62.62, 
        "humidity": 0.47, 
        "visibility": 10, 
        "summary": "Clear", 
        "apparentTemperature": 85.87, 
        "pressure": 1015.1, 
        "windSpeed": 16.71, 
        "cloudCover": 0.22, 
        "time": 1400716800, 
        "windBearing": 145, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.02, 
        "temperature": 82.31, 
        "icon": "clear-day", 
        "dewPoint": 63.46, 
        "humidity": 0.53, 
        "visibility": 10, 
        "summary": "Clear", 
        "apparentTemperature": 83.6, 
        "pressure": 1015.51, 
        "windSpeed": 16.23, 
        "cloudCover": 0.18, 
        "time": 1400720400, 
        "windBearing": 146, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.26, 
        "temperature": 79.06, 
        "icon": "clear-night", 
        "dewPoint": 64.21, 
        "humidity": 0.61, 
        "visibility": 10, 
        "summary": "Clear", 
        "apparentTemperature": 79.06, 
        "pressure": 1016.17, 
        "windSpeed": 15.4, 
        "cloudCover": 0.13, 
        "time": 1400724000, 
        "windBearing": 149, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.36, 
        "temperature": 76.11, 
        "icon": "clear-night", 
        "dewPoint": 64.64, 
        "humidity": 0.68, 
        "visibility": 10, 
        "summary": "Clear", 
        "apparentTemperature": 76.11, 
        "pressure": 1016.83, 
        "windSpeed": 14.41, 
        "cloudCover": 0.05, 
        "time": 1400727600, 
        "windBearing": 153, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.15, 
        "temperature": 73.6, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.05, 
        "humidity": 0.75, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 73.6, 
        "pressure": 1017.39, 
        "windSpeed": 13.28, 
        "cloudCover": 0.28, 
        "time": 1400731200, 
        "windBearing": 155, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 302.81, 
        "temperature": 71.7, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.37, 
        "humidity": 0.81, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 71.7, 
        "pressure": 1017.82, 
        "windSpeed": 12.37, 
        "cloudCover": 0.38, 
        "time": 1400734800, 
        "windBearing": 157, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 302.55, 
        "temperature": 69.56, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.56, 
        "humidity": 0.87, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 69.56, 
        "pressure": 1018.07, 
        "windSpeed": 11.41, 
        "cloudCover": 0.34, 
        "time": 1400738400, 
        "windBearing": 158, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 302.38, 
        "temperature": 68.54, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.64, 
        "humidity": 0.9, 
        "visibility": 9.06, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 68.54, 
        "pressure": 1018.13, 
        "windSpeed": 10.18, 
        "cloudCover": 0.5, 
        "time": 1400742000, 
        "windBearing": 160, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 302.29, 
        "temperature": 68.26, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.81, 
        "humidity": 0.92, 
        "visibility": 7.37, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 68.26, 
        "pressure": 1018.03, 
        "windSpeed": 9.02, 
        "cloudCover": 0.77, 
        "time": 1400745600, 
        "windBearing": 162, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 302.41, 
        "temperature": 68.23, 
        "icon": "cloudy", 
        "dewPoint": 66.04, 
        "humidity": 0.93, 
        "visibility": 5.47, 
        "summary": "Overcast", 
        "apparentTemperature": 68.23, 
        "pressure": 1017.94, 
        "windSpeed": 8.11, 
        "cloudCover": 0.98, 
        "time": 1400749200, 
        "windBearing": 163, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 302.97, 
        "temperature": 68.08, 
        "icon": "cloudy", 
        "dewPoint": 66.27, 
        "humidity": 0.94, 
        "visibility": 3.16, 
        "summary": "Overcast", 
        "apparentTemperature": 68.08, 
        "pressure": 1017.92, 
        "windSpeed": 7.36, 
        "cloudCover": 1, 
        "time": 1400752800, 
        "windBearing": 159, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.75, 
        "temperature": 67.85, 
        "icon": "fog", 
        "dewPoint": 66.35, 
        "humidity": 0.95, 
        "visibility": 0.64, 
        "summary": "Foggy", 
        "apparentTemperature": 67.85, 
        "pressure": 1017.97, 
        "windSpeed": 6.95, 
        "cloudCover": 1, 
        "time": 1400756400, 
        "windBearing": 151, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.24, 
        "temperature": 68.35, 
        "icon": "fog", 
        "dewPoint": 66.64, 
        "humidity": 0.94, 
        "visibility": 0.08, 
        "summary": "Foggy", 
        "apparentTemperature": 68.35, 
        "pressure": 1018.11, 
        "windSpeed": 7.02, 
        "cloudCover": 0.99, 
        "time": 1400760000, 
        "windBearing": 144, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.18, 
        "temperature": 69.69, 
        "icon": "partly-cloudy-day", 
        "precipType": "rain", 
        "humidity": 0.92, 
        "visibility": 2.65, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 69.69, 
        "pressure": 1018.39, 
        "windSpeed": 7.78, 
        "cloudCover": 0.93, 
        "time": 1400763600, 
        "windBearing": 141, 
        "precipIntensity": 0.0021, 
        "dewPoint": 67.16, 
        "precipProbability": 0.08
      }, 
      {
        "ozone": 303.84, 
        "temperature": 71.49, 
        "icon": "partly-cloudy-day", 
        "precipType": "rain", 
        "humidity": 0.88, 
        "visibility": 6.88, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 71.49, 
        "pressure": 1018.69, 
        "windSpeed": 8.81, 
        "cloudCover": 0.86, 
        "time": 1400767200, 
        "windBearing": 141, 
        "precipIntensity": 0.0031, 
        "dewPoint": 67.64, 
        "precipProbability": 0.17
      }, 
      {
        "ozone": 303.59, 
        "temperature": 73.54, 
        "icon": "partly-cloudy-day", 
        "precipType": "rain", 
        "humidity": 0.83, 
        "visibility": 10, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 73.54, 
        "pressure": 1018.93, 
        "windSpeed": 9.65, 
        "cloudCover": 0.8, 
        "time": 1400770800, 
        "windBearing": 142, 
        "precipIntensity": 0.0036, 
        "dewPoint": 68.02, 
        "precipProbability": 0.21
      }, 
      {
        "ozone": 303.53, 
        "temperature": 75.79, 
        "icon": "partly-cloudy-day", 
        "precipType": "rain", 
        "humidity": 0.77, 
        "visibility": 10, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 75.79, 
        "pressure": 1019.04, 
        "windSpeed": 10.31, 
        "cloudCover": 0.79, 
        "time": 1400774400, 
        "windBearing": 144, 
        "precipIntensity": 0.0033, 
        "dewPoint": 68.22, 
        "precipProbability": 0.17
      }, 
      {
        "ozone": 303.56, 
        "temperature": 77.85, 
        "icon": "partly-cloudy-day", 
        "precipType": "rain", 
        "humidity": 0.71, 
        "visibility": 10, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 77.85, 
        "pressure": 1019.02, 
        "windSpeed": 10.9, 
        "cloudCover": 0.8, 
        "time": 1400778000, 
        "windBearing": 145, 
        "precipIntensity": 0.0025, 
        "dewPoint": 67.86, 
        "precipProbability": 0.08
      }, 
      {
        "ozone": 303.7, 
        "temperature": 80.27, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 67.87, 
        "humidity": 0.66, 
        "visibility": 10, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 82.87, 
        "pressure": 1018.8, 
        "windSpeed": 11.57, 
        "cloudCover": 0.76, 
        "time": 1400781600, 
        "windBearing": 145, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.03, 
        "temperature": 82.64, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 67.84, 
        "humidity": 0.61, 
        "visibility": 10, 
        "summary": "Mostly Cloudy", 
        "apparentTemperature": 85.6, 
        "pressure": 1018.21, 
        "windSpeed": 12.64, 
        "cloudCover": 0.63, 
        "time": 1400785200, 
        "windBearing": 141, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.47, 
        "temperature": 84.86, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 67.69, 
        "humidity": 0.57, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 87.99, 
        "pressure": 1017.41, 
        "windSpeed": 13.7, 
        "cloudCover": 0.47, 
        "time": 1400788800, 
        "windBearing": 137, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.75, 
        "temperature": 85.93, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 67.29, 
        "humidity": 0.54, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 88.94, 
        "pressure": 1016.73, 
        "windSpeed": 14.4, 
        "cloudCover": 0.38, 
        "time": 1400792400, 
        "windBearing": 136, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.78, 
        "temperature": 85.85, 
        "icon": "partly-cloudy-day", 
        "dewPoint": 67.19, 
        "humidity": 0.54, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 88.8, 
        "pressure": 1016.25, 
        "windSpeed": 14.78, 
        "cloudCover": 0.43, 
        "time": 1400796000, 
        "windBearing": 136, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.65, 
        "temperature": 84.92, 
        "icon": "partly-cloudy-day", 
        "precipType": "rain", 
        "humidity": 0.56, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 87.85, 
        "pressure": 1015.92, 
        "windSpeed": 14.93, 
        "cloudCover": 0.52, 
        "time": 1400799600, 
        "windBearing": 137, 
        "precipIntensity": 0.0007, 
        "dewPoint": 67.29, 
        "precipProbability": 0.01
      }, 
      {
        "ozone": 304.39, 
        "temperature": 83.36, 
        "icon": "partly-cloudy-day", 
        "precipType": "rain", 
        "humidity": 0.58, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 86.12, 
        "pressure": 1015.84, 
        "windSpeed": 14.77, 
        "cloudCover": 0.56, 
        "time": 1400803200, 
        "windBearing": 139, 
        "precipIntensity": 0.0009, 
        "dewPoint": 67.25, 
        "precipProbability": 0.01
      }, 
      {
        "ozone": 303.85, 
        "temperature": 80.95, 
        "icon": "partly-cloudy-day", 
        "precipType": "rain", 
        "humidity": 0.62, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 83.32, 
        "pressure": 1016.22, 
        "windSpeed": 14.19, 
        "cloudCover": 0.5, 
        "time": 1400806800, 
        "windBearing": 142, 
        "precipIntensity": 0.0009, 
        "dewPoint": 66.77, 
        "precipProbability": 0.01
      }, 
      {
        "ozone": 303.18, 
        "temperature": 77.99, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 66.09, 
        "humidity": 0.67, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 77.99, 
        "pressure": 1016.9, 
        "windSpeed": 13.37, 
        "cloudCover": 0.41, 
        "time": 1400810400, 
        "windBearing": 148, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 302.85, 
        "temperature": 75.27, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.66, 
        "humidity": 0.72, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 75.27, 
        "pressure": 1017.53, 
        "windSpeed": 12.51, 
        "cloudCover": 0.37, 
        "time": 1400814000, 
        "windBearing": 154, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.12, 
        "temperature": 72.91, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 65.81, 
        "humidity": 0.78, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 72.91, 
        "pressure": 1017.97, 
        "windSpeed": 11.97, 
        "cloudCover": 0.4, 
        "time": 1400817600, 
        "windBearing": 157, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 303.72, 
        "temperature": 70.99, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 66.3, 
        "humidity": 0.85, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 70.99, 
        "pressure": 1018.29, 
        "windSpeed": 11.47, 
        "cloudCover": 0.47, 
        "time": 1400821200, 
        "windBearing": 159, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }, 
      {
        "ozone": 304.31, 
        "temperature": 69.69, 
        "icon": "partly-cloudy-night", 
        "dewPoint": 66.63, 
        "humidity": 0.9, 
        "visibility": 10, 
        "summary": "Partly Cloudy", 
        "apparentTemperature": 69.69, 
        "pressure": 1018.53, 
        "windSpeed": 10.88, 
        "cloudCover": 0.57, 
        "time": 1400824800, 
        "windBearing": 159, 
        "precipIntensity": 0, 
        "precipProbability": 0
      }
    ], 
    "summary": "Mostly cloudy until tomorrow afternoon."
  }, 
  "currently": {
    "ozone": 309.58, 
    "temperature": 71.29, 
    "dewPoint": 66.99, 
    "nearestStormDistance": 34, 
    "cloudCover": 0.77, 
    "humidity": 0.86, 
    "nearestStormBearing": 335, 
    "summary": "Mostly Cloudy", 
    "apparentTemperature": 71.29, 
    "pressure": 1016.25, 
    "windSpeed": 8.93, 
    "precipProbability": 0, 
    "visibility": 9.68, 
    "time": 1400653274, 
    "windBearing": 163, 
    "precipIntensity": 0, 
    "icon": "partly-cloudy-night"
  }, 
  "longitude": -97.7707, 
  "flags": {
    "lamp-stations": [
      "KATT", 
      "KAUS", 
      "KBMQ", 
      "KGTU", 
      "KHYI"
    ], 
    "sources": [
      "nwspa", 
      "isd", 
      "nearest-precip", 
      "fnmoc", 
      "sref", 
      "rtma", 
      "rap", 
      "nam", 
      "cmc", 
      "gfs", 
      "madis", 
      "lamp", 
      "darksky"
    ], 
    "units": "us", 
    "madis-stations": [
      "ABUT2", 
      "AS425", 
      "AU165", 
      "C6155", 
      "CACT2", 
      "D9484", 
      "E0214", 
      "E0335", 
      "E2049", 
      "E2510", 
      "E3714", 
      "E4737", 
      "JLCT2", 
      "KATT", 
      "LWAT2", 
      "UR165"
    ], 
    "darksky-stations": [
      "KGRK"
    ], 
    "isd-stations": [
      "722540-13958", 
      "722544-13958", 
      "722545-99999", 
      "999999-13958", 
      "999999-93923"
    ]
  }, 
  "daily": {
    "icon": "rain", 
    "data": [
      {
        "apparentTemperatureMinTime": 1400670000, 
        "cloudCover": 0.54, 
        "temperatureMin": 69.81, 
        "summary": "Mostly cloudy until afternoon.", 
        "dewPoint": 64.91, 
        "apparentTemperatureMax": 88.71, 
        "temperatureMax": 87.88, 
        "temperatureMaxTime": 1400706000, 
        "windBearing": 160, 
        "moonPhase": 0.75, 
        "visibility": 9.82, 
        "sunsetTime": 1400721789, 
        "pressure": 1016.57, 
        "precipProbability": 0, 
        "apparentTemperatureMin": 69.81, 
        "precipIntensityMax": 0, 
        "icon": "partly-cloudy-day", 
        "apparentTemperatureMaxTime": 1400706000, 
        "humidity": 0.68, 
        "ozone": 306.5, 
        "windSpeed": 13.59, 
        "time": 1400648400, 
        "precipIntensity": 0, 
        "sunriseTime": 1400672105, 
        "temperatureMinTime": 1400670000
      }, 
      {
        "apparentTemperatureMinTime": 1400756400, 
        "precipType": "rain", 
        "cloudCover": 0.65, 
        "precipIntensityMaxTime": 1400770800, 
        "temperatureMin": 67.85, 
        "summary": "Foggy in the morning.", 
        "dewPoint": 66.81, 
        "apparentTemperatureMax": 88.94, 
        "temperatureMax": 85.93, 
        "temperatureMaxTime": 1400792400, 
        "windBearing": 146, 
        "moonPhase": 0.79, 
        "visibility": 8.2, 
        "sunsetTime": 1400808227, 
        "pressure": 1017.74, 
        "precipProbability": 0.21, 
        "apparentTemperatureMin": 67.85, 
        "precipIntensityMax": 0.0036, 
        "icon": "fog", 
        "apparentTemperatureMaxTime": 1400792400, 
        "humidity": 0.76, 
        "ozone": 303.58, 
        "windSpeed": 11.07, 
        "time": 1400734800, 
        "precipIntensity": 0.0013, 
        "sunriseTime": 1400758477, 
        "temperatureMinTime": 1400756400
      }, 
      {
        "apparentTemperatureMinTime": 1400842800, 
        "precipType": "rain", 
        "cloudCover": 0.76, 
        "precipIntensityMaxTime": 1400889600, 
        "temperatureMin": 67.99, 
        "summary": "Foggy in the morning.", 
        "dewPoint": 65.13, 
        "apparentTemperatureMax": 85.95, 
        "temperatureMax": 84.66, 
        "temperatureMaxTime": 1400878800, 
        "windBearing": 150, 
        "moonPhase": 0.83, 
        "visibility": 7.49, 
        "sunsetTime": 1400894665, 
        "pressure": 1017.32, 
        "precipProbability": 0.06, 
        "apparentTemperatureMin": 67.99, 
        "precipIntensityMax": 0.0014, 
        "icon": "fog", 
        "apparentTemperatureMaxTime": 1400878800, 
        "humidity": 0.73, 
        "ozone": 309.96, 
        "windSpeed": 10.4, 
        "time": 1400821200, 
        "precipIntensity": 0.0007, 
        "sunriseTime": 1400844850, 
        "temperatureMinTime": 1400842800
      }, 
      {
        "apparentTemperatureMinTime": 1400922000, 
        "precipType": "rain", 
        "cloudCover": 0.84, 
        "precipIntensityMaxTime": 1400950800, 
        "temperatureMin": 65.23, 
        "summary": "Mostly cloudy throughout the day.", 
        "dewPoint": 65.48, 
        "apparentTemperatureMax": 88.59, 
        "temperatureMax": 85.35, 
        "temperatureMaxTime": 1400972400, 
        "windBearing": 152, 
        "moonPhase": 0.87, 
        "visibility": 9.08, 
        "sunsetTime": 1400981101, 
        "pressure": 1015.56, 
        "precipProbability": 0.19, 
        "apparentTemperatureMin": 65.23, 
        "precipIntensityMax": 0.0041, 
        "icon": "partly-cloudy-day", 
        "apparentTemperatureMaxTime": 1400972400, 
        "humidity": 0.75, 
        "ozone": 317.65, 
        "windSpeed": 10.49, 
        "time": 1400907600, 
        "precipIntensity": 0.0023, 
        "sunriseTime": 1400931225, 
        "temperatureMinTime": 1400922000
      }, 
      {
        "apparentTemperatureMinTime": 1401015600, 
        "precipType": "rain", 
        "cloudCover": 0.8, 
        "precipIntensityMaxTime": 1401058800, 
        "temperatureMin": 68.37, 
        "summary": "Drizzle throughout the day.", 
        "dewPoint": 67.28, 
        "apparentTemperatureMax": 90.64, 
        "temperatureMax": 86.41, 
        "temperatureMaxTime": 1401055200, 
        "windBearing": 153, 
        "moonPhase": 0.9, 
        "sunsetTime": 1401067538, 
        "pressure": 1014.03, 
        "precipProbability": 0.55, 
        "apparentTemperatureMin": 68.37, 
        "precipIntensityMax": 0.0089, 
        "icon": "rain", 
        "apparentTemperatureMaxTime": 1401055200, 
        "humidity": 0.76, 
        "ozone": 311.39, 
        "windSpeed": 10.76, 
        "time": 1400994000, 
        "precipIntensity": 0.0058, 
        "sunriseTime": 1401017601, 
        "temperatureMinTime": 1401015600
      }, 
      {
        "apparentTemperatureMinTime": 1401102000, 
        "precipType": "rain", 
        "cloudCover": 0.75, 
        "precipIntensityMaxTime": 1401105600, 
        "temperatureMin": 69.91, 
        "summary": "Drizzle throughout the day.", 
        "dewPoint": 69.2, 
        "apparentTemperatureMax": 90.37, 
        "temperatureMax": 85.42, 
        "temperatureMaxTime": 1401145200, 
        "windBearing": 165, 
        "moonPhase": 0.94, 
        "sunsetTime": 1401153974, 
        "pressure": 1013.78, 
        "precipProbability": 0.56, 
        "apparentTemperatureMin": 69.91, 
        "precipIntensityMax": 0.0082, 
        "icon": "rain", 
        "apparentTemperatureMaxTime": 1401145200, 
        "humidity": 0.78, 
        "ozone": 319.13, 
        "windSpeed": 10.18, 
        "time": 1401080400, 
        "precipIntensity": 0.0074, 
        "sunriseTime": 1401103978, 
        "temperatureMinTime": 1401102000
      }, 
      {
        "apparentTemperatureMinTime": 1401188400, 
        "precipType": "rain", 
        "cloudCover": 0.6, 
        "precipIntensityMaxTime": 1401249600, 
        "temperatureMin": 71.1, 
        "summary": "Light rain until afternoon, starting again in the evening.", 
        "dewPoint": 69.53, 
        "apparentTemperatureMax": 95.42, 
        "temperatureMax": 89.52, 
        "temperatureMaxTime": 1401231600, 
        "windBearing": 174, 
        "moonPhase": 0.97, 
        "sunsetTime": 1401240409, 
        "pressure": 1013.12, 
        "precipProbability": 0.63, 
        "apparentTemperatureMin": 71.1, 
        "precipIntensityMax": 0.0101, 
        "icon": "rain", 
        "apparentTemperatureMaxTime": 1401231600, 
        "humidity": 0.75, 
        "ozone": 322.88, 
        "windSpeed": 9.54, 
        "time": 1401166800, 
        "precipIntensity": 0.006, 
        "sunriseTime": 1401190356, 
        "temperatureMinTime": 1401188400
      }, 
      {
        "apparentTemperatureMinTime": 1401274800, 
        "precipType": "rain", 
        "cloudCover": 0.41, 
        "precipIntensityMaxTime": 1401267600, 
        "temperatureMin": 70.24, 
        "summary": "Light rain in the morning.", 
        "dewPoint": 67.99, 
        "apparentTemperatureMax": 98.65, 
        "temperatureMax": 92.97, 
        "temperatureMaxTime": 1401310800, 
        "windBearing": 177, 
        "moonPhase": 0.01, 
        "sunsetTime": 1401326844, 
        "pressure": 1011.63, 
        "precipProbability": 0.8, 
        "apparentTemperatureMin": 70.24, 
        "precipIntensityMax": 0.0266, 
        "icon": "rain", 
        "apparentTemperatureMaxTime": 1401310800, 
        "humidity": 0.67, 
        "ozone": 317.02, 
        "windSpeed": 8.73, 
        "time": 1401253200, 
        "precipIntensity": 0.0089, 
        "sunriseTime": 1401276736, 
        "temperatureMinTime": 1401274800
      }
    ], 
    "summary": "Light rain on Sunday through Wednesday, with temperatures bottoming out at 85\u00b0F on Friday."
  }, 
  "offset": -5, 
  "latitude": 30.3389, 
  "timezone": "America/Chicago", 
  "minutely": {
    "icon": "partly-cloudy-night", 
    "data": [
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653260
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653320
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653380
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653440
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653500
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653560
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653620
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653680
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653740
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653800
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653860
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653920
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400653980
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654040
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654100
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654160
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654220
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654280
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654340
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654400
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654460
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654520
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654580
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654640
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654700
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654760
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654820
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654880
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400654940
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655000
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655060
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655120
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655180
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655240
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655300
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655360
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655420
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655480
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655540
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655600
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655660
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655720
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655780
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655840
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655900
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400655960
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656020
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656080
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656140
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656200
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656260
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656320
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656380
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656440
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656500
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656560
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656620
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656680
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656740
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656800
      }, 
      {
        "precipIntensity": 0, 
        "precipProbability": 0, 
        "time": 1400656860
      }
    ], 
    "summary": "Mostly cloudy for the hour."
  }
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
