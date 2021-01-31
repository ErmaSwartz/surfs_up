import datetime as dt 
import numpy as np 
import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# access the sqlite database 
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
#reflect the database 
Base.prepare(engine, reflect=True)
#save our references to each table 
Measurement = Base.classes.measurement
Station = Base.classes.station
#create a link from python to our database 
session = Session(engine)
#define our flask app
app = Flask(__name__)
#define the welcome route
@app.route("/")
#add routing number information for each route 
#create a function 
def welcome():
    return( 
        '''
    Welcome to the Climate Analysis API!
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end''')

# create a route for precipitation analysis 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # calculates the date one year ago from the most recent date in database 
  prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query to get the date and precipiation for the previous year 
  precipitation = session.query(Measurement.date, Measurement.prcp).\
  filter(Measurement.date >= prev_year).all()
    # create a dictionary with the date as the key and the precipitation as the value
  precip = {date: prcp for date, prcp in precipitation}
  #make it a json file 
  return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    #create a query that akkiws us to get all the stations in our database 
    results = session.query(Station.station).all()
     #convert our unraveled results into a list 
    ## using the list function
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
  
  #return the temperature observations for the previous year 
@app.route("/api/vi.0/tobs")
  #create a function 
def temp_monthly():
    #calculate the date one year from the last date in the database 
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #query the primary station for all the temperature observations from the previous year 
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
      #unravel the results into a one dimensional array 
      #convert array into a list 
    temps = list(np.ravel(results))
    #jsonify our temps  
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == "__main__":
  app.run(debug=True)
