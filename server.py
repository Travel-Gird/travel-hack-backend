from flask import Flask, request, jsonify

import app
import db
import config


server = Flask(__name__)


@server.route('/sightsigns', methods=['GET'])
def get_places_endpoint():
    return jsonify({'sightsigns': db.get_places_from_db()}), 200


@server.route('/routes', methods=['GET'])
def get_routes_endpoint():
    request_data = request.args
    response_data = app.generate_routes(user_data=request_data)
    return jsonify({'routes': response_data}), 200


@server.route('/recommended_routes', methods=['GET'])
def get_recommended_routes_endpoint():
    request_data = request.args
    response_data = app.recommend_routes(user_data=request_data)
    return jsonify({'recommended_routes': response_data}), 200


if __name__ == '__main__':
    server.run(host=config.HOST,
               port=config.PORT,
               debug=True)
