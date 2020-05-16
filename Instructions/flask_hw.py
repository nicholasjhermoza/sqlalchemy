from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

flask_hw = Flask(__name__)
#ROOT
@flask_hw.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )

#Convert the query results to a dictionary using date as the key and prcp as the value.
#station = dict{'date' : 'prcp' }
#Return the JSON representation of your dictionary.
@flask_hw.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > one_year_ago).\
    order_by(Measurement.date).all()

#Return a JSON list of stations from the dataset.
    prcp = [{element[0]:element[1]} for element in prcp_data]
    return jsonify(prcp)
# #Query the dates and temperature observations of the most active station for the last year of data.
@flask_hw.route("/api/v1.0/stations")
def stations():
    s_results = session.query(Station.station, Station.name).all()
    station_litst = list(np.ravel(s_results))
    return jsonify(station_litst)
# #Return a JSON list of temperature observations (TOBS) for the previous year.
@flask_hw.route("/api/v1.0/tobs")
def TOBS():
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    t_results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= one_year_ago).all()
    temps = list(np.ravel(t_results))
    return jsonify(temps)
@flask_hw.route("/api/v1.0/<start_date>")
def start_date(start_date):
    result = session.query(func.min(Measurement.tobs),
    func.avg(Measurement.tobs), 
    func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    return jsonify(result)
    
@flask_hw.route("/api/v1.0/<start_date>/<end_date>")
def end_date(start_date, end_date):
    result1 = session.query(func.min(Measurement.tobs),
    func.avg(Measurement.tobs), 
    func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(result1)

if __name__ == "__main__":
    flask_hw.run(debug=True)