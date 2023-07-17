from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# Mongo Connection string

mongo_uri = "mongodb+srv://pilotcanopy:AdityaMichael@canopy-pilot-database.ixg30z7.mongodb.net/canopy-pilot-database?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client.get_database()

# Collection name for farm sensor data
collection = db.farm_sensor_data


# Endpoint to write data from farm sensors
@app.route('/api/farm/sensor', methods=['POST'])
def write_sensor_data():
    data = request.get_json()
    collection.insert_one(data)
    return jsonify({"message": "Data written successfully"}), 201


# Endpoint to read the latest farm sensor data
@app.route('/api/farm/sensor/latest', methods=['GET'])
def get_latest_sensor_data():
    data = collection.find().sort('_id', -1).limit(1)
    latest_data = next(data, None)
    if latest_data:
        latest_data.pop('_id')  # Remove the MongoDB ObjectId from the response
        return jsonify(latest_data)
    else:
        return jsonify({"message": "No data found"}), 404


# Endpoint to read all farm sensor data
@app.route('/api/farm/sensor/all', methods=['GET'])
def get_all_sensor_data():
    all_data = list(collection.find({}, {'_id': 0}))
    if all_data:
        return jsonify(all_data)
    else:
        return jsonify({"message": "No data found"}), 404


#if __name__ == '__main__':
#    app.run(debug=True)
