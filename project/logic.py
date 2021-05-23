from dotenv import load_dotenv
from flask import Flask, Blueprint, request, json, jsonify, render_template, make_response
import pandas as pd
import geopandas as gpd
import os

def get_cta_isos():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data/chicago", "cta_5_min.geojson")
    data = json.load(open(json_url))
    return data

def get_ogilvie_isos():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data/chicago", "chicago_commuter_ogilvie.geojson")
    data = json.load(open(json_url))
    return data

def get_union_isos():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data/chicago", "chicago_commuter_union.geojson")
    data = json.load(open(json_url))
    return data

def get_restaurants():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data/chicago", "chicago_restaurants.geojson")
    data = json.load(open(json_url))
    return data
