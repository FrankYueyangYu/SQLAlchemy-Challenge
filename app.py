import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = base.classes.measurement
Station = base.classes.station
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def home():
    return (
    	f"Home<br/>"
    	f"Routes:<br/>"
    	f"/api/v1.0/precipitation<br/>"
    	f"/api/v1.0/stations<br/>"
    	f"/api/v1.0/tobs<br/>"
    	f"/api/v1.0/start<br/>"
    	f"/api/v1.0/start/end")


@app.route('/api/v1.0/precipitation')
def prcp():
	session = Session(engine)
	results = session.query(Measurement.date, Measurement.prcp).all()	
	session.close()
	prcpdate = []
	for date, prcp in results:
		Measurement_dict = {}
		Measurement_dict["date"] = date
		Measurement_dict["prcp"] = prcp
		prcpdate.append(Measurement_dict)
	return jsonify(prcpdate)


@app.route('/api/v1.0/stations')
def stations():
	session = Session(engine)
	results = session.query(Station.station,Station.name).all()
	session.close()
	stationlist = list(np.ravel(results))
	return jsonify(stationlist)

@app.route('/api/v1.0/tobs')
def tobs():
	session = Session(engine)
	yearbefore = dt.date(2017,8,18) - dt.timedelta(days=365)
	results = session.query(Measurement.tobs).\
    filter(Measurement.date >= yearbefore).all()
	session.close()
	Tobs = list(np.ravel(results))
	return jsonify(Tobs)


@app.route("/api/v1.0/start")
def start():
	session = Session(engine) 
	start_date = dt.date(2011,3,1)
	sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
	results = session.query(*sel).filter(Measurement.date >= start_date).all()
	session.close()
	tobstart = list(np.ravel(results))
	return jsonify(tobstart)


@app.route('/api/v1.0/start/end')
def start_end():
	session = Session(engine)
	start_date = dt.date(2011,5,2)
	end_date = dt.date(2013,2,6)
	sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
	results = session.query(*sel).filter((Measurement.date > start_date) & (Measurement.date < end_date)).all()
	session.close()
	startendtob = list(np.ravel(results))
	return jsonify(startendtob)
