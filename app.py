import fb


def generate_routes(user_data) -> dict:
    user_fb = fb.Facebook(access_token=user_data['access_token'],
                          user_id=user_data['user_id'])
    routes_data = {}
    return parse_routes(routes_data)


def parse_routes(routes_data) -> dict:
    return {'routes': [{'image': '',
                        'cityName': 'Moscow',
                        'timeTable': [{'time': '',
                                       'place': '',
                                       'placeImage': ''}]}]}
