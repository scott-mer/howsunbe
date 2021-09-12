from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
from plotly import graph_objs
import plotly.express as px
import datetime
from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP

app = Flask(__name__)

@app.route('/process', methods=['POST', 'GET'])
def process():
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    timezone = request.form['timezone']
    model = request.form['model']
    return generate_plot(latitude, longitude, timezone, model)
   
@app.route('/')
def index():
    return render_template('index.html',  graphJSON=generate_plot())

def generate_plot(latitude=32.2, longitude=-110.9, timezone="US/Arizona", model="GFS"):
    start = pd.Timestamp(datetime.date.today(), tz=timezone)
    end = start + pd.Timedelta(days=7)
    if model == "GFS":
        m = GFS()
    elif model == "NAM":
        m = NAM()
    elif model == "NDFD":
        m = NDFD()
    elif model == "HRRR":
        m = HRRR()
    elif model == "RAP":
        m = RAP()
    df = m.get_processed_data(latitude, longitude, start, end)
    fig = px.line(df, x=df.index, y=["ghi","dni","dhi"])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
