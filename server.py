from flask import Flask, request

import config


server = Flask(__name__)


@server.route('/routes', methods=['GET'])
def get_routes_endpoint():
    return '', 200


def parse_data(data):
    pass


if __name__ == '__main__':
    server.run(host='0.0.0.0',
               port=config.PORT,
               debug=True)
