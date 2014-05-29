from flask import Flask, request, render_template
import urllib2
import json
app = Flask(__name__)

WALK_TIME_SECS = 180
MBTA_REDLINE_URL = 'http://developer.mbta.com/lib/rthr/red.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next-arrival')
def next_arrival():
    try:
        redline = json.loads(urllib2.urlopen(MBTA_REDLINE_URL).read())
        
        # filter  trips headed towards Alewife
        alewife_trips = [trip for trip in redline['TripList']['Trips'] if trip['Destination'] == 'Alewife']
        
        # get only the predictions 
        predictions = []
        for trip in alewife_trips:
            predictions += trip['Predictions']

        # filter stops for 'Andrew' and greater than time it takes to walk to T
        andrew_stops = [stop for stop in predictions if stop['Stop'] == 'Andrew' and stop['Seconds'] > WALK_TIME_SECS]
        
        # sort and pick closest
        sorted_andrew = sorted(andrew_stops, key=lambda stop: stop['Seconds'])
        return str(sorted_andrew[0]['Seconds'] / 60) if len(sorted_andrew) > 0 else "-1"

    except:
        return "-1"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7700, debug=True)

