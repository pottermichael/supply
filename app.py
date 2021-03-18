from flask import Flask, request, json, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

#https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pgsuper007@localhost:5432/cars_api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #get rid of annoying warning
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/base', methods=["GET"])
def base():
    return render_template("base.html")

@app.route('/denver', methods=["GET"])
def denver():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "nashville_bldg_footprints.geojson")
    data = json.load(open(json_url))
    print(type(data))
    print(data)
    return render_template("denver.html",data=data)

@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/form', methods=["GET","POST"])
def form():
    return render_template("form.html")

@app.route('/landing', methods=["GET"])
def landing():
    return render_template("landing.html")

@app.route('/salesforce', methods=["GET"])
def salesforce():
    return render_template("salesforce.html")


"""
LEASING FOR NEW BUILDINGS

"""
@app.route('/map', methods=["GET"])
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

@app.route('/cars', methods=['POST', 'GET'])
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

@app.route('/cars/<car_id>', methods=['GET','PUT','DELETE'])
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
    app.run(debug=True)
