from flask import Flask, request, render_template
import urllib2
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/next-arrival')
def next_arrival():
    try:
        jsonurl = urllib2.urlopen('http://developer.mbta.com/lib/rthr/red.json')
    except:
        return "-1"
    redline = json.loads(jsonurl.read()) 
    alewife_trips = [trip for trip in redline['TripList']['Trips'] if trip['Destination'] == 'Alewife']
    predictions = []
    for trip in alewife_trips:
        predictions += trip['Predictions']
    andrew_stops = [stop for stop in predictions if stop['Stop'] == 'Andrew']
    return str(sorted(andrew_stops, key=lambda x: x['Seconds'])[0]['Seconds'] / 60)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

