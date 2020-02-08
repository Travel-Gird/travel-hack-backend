from flask import Flask, request, jsonify

import app
import config


server = Flask(__name__)


@server.route('/routes', methods=['GET'])
def get_routes_endpoint():
    request_data = request.args
    response_data = app.generate_routes(user_data=request_data)
    return jsonify(response_data), 200


if __name__ == '__main__':
    server.run(host=config.HOST,
               port=config.PORT,
               debug=True)
