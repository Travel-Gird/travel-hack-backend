from flask import Flask, request, jsonify

import routes
import db
import fb
import config

server = Flask(__name__)


@server.route('/sightsigns', methods=['GET'])
def get_places_endpoint():
    request_data = request.args
    places = db.get_places_from_db(city_name=request_data['country'])
    return jsonify({'sightsigns': places}), 200


@server.route('/routes', methods=['GET', 'POST'])
def get_routes_endpoint():
    if request.method == 'GET':
        request_data = request.args
        response_data = routes.generate_routes(
            places_data=request_data.getlist('sightsigns')
        )
        fb.create_fb_user(user_id=request_data['userId'],
                          access_token=request_data['token'],
                          budget=request_data['budjet'],
                          activity=request_data['activity'])
        return jsonify({'routes': response_data}), 200
    elif request.method == 'POST':
        request_data = request.json
        routes.rate_route(user_facebook_id=request_data['userId'],
                          route_id=request_data['routeId'])
        return '', 201


@server.route('/recommended_routes', methods=['GET'])
def get_recommended_routes_endpoint():
    request_data = request.args
    response_data = routes.recommend_routes(user_data=request_data)
    return jsonify({'routes': response_data}), 200


if __name__ == '__main__':
    server.run(host=config.HOST,
               port=config.PORT,
               debug=True)
