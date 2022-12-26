from ryanair import Ryanair
from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/flights', methods=['GET'])
def respond():
    not_go = ['Italy', 'Croatia', 'United Kingdom', 'Austria', 'Belgium','Netherlands', 'Estonia', 'Latvia', 'Lithuania',
              'Germany', 'Spain', 'France', 'Bulgaria', 'Denmark', 'Ireland']
    response = {}
    ryanair = Ryanair("EUR")
    date_compare = request.args.get("date", "2023-04-22")
    return_date = request.args.get("returnDate", "2023-04-25")
    date_time_obj = request.args.get("minTime", '09:00:00')
    date_time_obj = datetime.strptime(date_time_obj, '%H:%M:%S')
    not_go_list = request.args.get("notTo", not_go)
    not_go_list = tuple(not_go_list)
    max_date = request.args.get("maxTime", '15:59:00')
    max_date = datetime.strptime(max_date, '%H:%M:%S')
    from_airports = request.args.get("from", 'BGY')
    from_airports = from_airports.split(',')


    filtered = {}
    for airport in from_airports:
        flights = ryanair.get_return_flights(airport, date_compare, date_compare, return_date, return_date)
        print(flights)
        f = filter(lambda trip: not trip.outbound.destinationFull.endswith(not_go_list) and
                                date_time_obj.time() < trip.outbound.departureTime.time() < max_date.time() and
                                trip.totalPrice < 120, flights)
        filtered[airport] = list(f)

    response["flights"] = filtered
    # Return the response in json format
    return jsonify(response)


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)

# for f in filtered: print(f.destinationFull+"\t\t\t\t"+str(f.price)+"\t"+str(f.departureTime.time()))
