from flask import Flask, request, render_template
import urllib2
import json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next-arrival')
def next_arrival():
    try:
        jsonurl = urllib2.urlopen('http://developer.mbta.com/lib/rthr/red.json')
    except:
        return "-1"
    redline = json.loads(jsonurl.read()) 
    # filter  trips headed towards Alewife
    alewife_trips = [trip for trip in redline['TripList']['Trips'] if trip['Destination'] == 'Alewife']
    # get only the predictions 
    predictions = [trip['Predictions'] for trip in alewife_trips]
    # filter stops for 'Andrew'
    andrew_stops = [stop for stop in predictions if stop['Stop'] == 'Andrew']
    # sort and grab the first stop seconds
    return str(sorted(andrew_stops, key=lambda stop: stop['Seconds'])[0]['Seconds'] / 60)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

