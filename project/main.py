from dotenv import load_dotenv
from flask import Flask, Blueprint, request, json, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd
import geopandas as gpd
import os

#https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/

from . import db

main = Blueprint('main', __name__ )

migrate = Migrate(main, db)

@main.route('/base', methods=["GET"])
def base():
    return render_template("base.html")

@main.route('/signin', methods=["GET"])
def signin():
    user = {'username': 'Miguel'}
    return render_template("login.html",user=user)

@main.route('/profile')
def profile():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return 'Profile'

@main.route('/denver', methods=["GET"])
def denver():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "denver_clear.geojson")
    data = json.load(open(json_url))
    return render_template("denver.html",data=data)


@main.route('/charlotte', methods=["GET"])
def charlotte():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "charlotte_clean.geojson")
    data = json.load(open(json_url))
    return render_template("charlotte.html",data=data)


@main.route('/denver_cbd', methods=["GET"])
def denver_cbd():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "denver_fixed_supply.geojson")
    data = json.load(open(json_url))
    #gdf = gpd.GeoDataFrame(open(json_url),geometry='geometry')
    #filter = gdf[gdf['use']=="office"]
    print("filter results")
    #print(gdf)
    print(type(data))
    print(data)
    return render_template("denver_cbd.html",data=data)

def get_isos():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "cta_5_min.geojson")
    data = json.load(open(json_url))
    return data

@main.route('/chicago', methods=["GET"])
def chicago():
    isos = get_isos()
    print(isos)
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "chicago_supply_final.geojson")
    data = json.load(open(json_url))
    #gdf = gpd.GeoDataFrame(open(json_url),geometry='geometry')
    #filter = gdf[gdf['use']=="office"]
    print("filter results")
    #print(gdf)
    print(type(data))
    print(data)
    return render_template("chicago.html",data=data, isos=isos)

@main.route('/geo', methods=["GET"])
def geojson_to_gpd():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "denver_clear.geojson")
    gdf = gpd.read_file(json_url,geometry="geometry",crs="EPSG:4326")
    gdf['center'] = gdf['geometry'].centroid
    print(gdf.columns)
    return render_template("geo.html",data=gdf)

@main.route('/', methods=["GET"])
@main.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@main.route('/form', methods=["GET","POST"])
def form():
    return render_template("form.html")

@main.route('/landing', methods=["GET"])
def landing():
    return render_template("landing.html")

@main.route('/salesforce', methods=["GET"])
def salesforce():
    return render_template("salesforce.html")


"""
LEASING FOR NEW BUILDINGS

"""
@main.route('/map', methods=["GET"])
def map():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "nashville_bldg_footprints.geojson")
    data = json.load(open(json_url))
    print(type(data))
    print(data)
    return render_template("map.html", data=data)

class DemandModel(db.Model):
    __tablename__ = 'leases'

    id = db.Column(db.Integer, primary_key=True)
    tenant = db.Column(db.String())
    area = db.Column(db.Integer())
    building = db.Column(db.String())
    broker_firm = db.Column(db.String())
    broker_lead = db.Column(db.String())
    desc = db.Column(db.String())

    def __init__(self,tenant,area,building,broker_firm,broker_lead,desc):
        self.tenant = tenant
        self.area = area
        self.building = building
        self.broker_firm = broker_firm
        self.broker_lead = broker_lead
        self.desc = desc

    def __repr__(self):
        return f"<leases {self.tenant}>"

"""
CARS EXAMPLE CODE

"""

class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self,name,model,doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Car {self.name}>"

@main.route('/cars', methods=['POST', 'GET'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_car = CarsModel(name=data['name'], model=data['model'], doors=data['doors'])

            db.session.add(new_car)
            db.session.commit()

            return jsonify(f"car {new_car.name} has been created successfully.")
        else:
            return "The request payload is not in JSON format"

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars] #list comprehension for dictionary

        return jsonify({"count": len(results), "cars": results, "message": "success"})

@main.route('/cars/<car_id>', methods=['GET','PUT','DELETE'])
def handle_car(car_id):
    car = CarsModel.query.get_or_404(car_id)

    if request.method == 'GET':
        response = {
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return jsonify({"message": "success", "car": response})

    elif request.method == "PUT":
        data = request.get_json()
        car.name = data['name']
        car.model = data['model']
        car.doors = data['doors']
        db.session.add(car)
        db.session.commit()
        return jsonify({"message": f"car {car.name} successfully updated"})

    elif request.method == "Delete":
        db.session.delete(car)
        db.session.commit()
        return jsonify({"message": f"Car {car.name} successfully deleted."})

"""
RUN APP

"""

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
