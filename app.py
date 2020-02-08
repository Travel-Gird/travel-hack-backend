import fb


def generate_routes(user_data: dict) -> dict:
    route_timestamp = 1581321600
    timestamp_shift = 60 * 24 * 24 / len(user_data['places'])
    route_data = {'image': 'https://s0.rbk.ru/v6_top_pics/media/img/7/59/755060771782597.jpg',
                  'cityName': 'San Francisco',
                  'timeTable': []}
    for place_id in user_data['places']:
        place_data = place_id
        route_chunk = {'time': str(route_timestamp),
                       'place': 'Golden Gate Bridge',
                       'placeImage': 'https://top10.travel/wp-content/uploads/2017/02/most-zolotye-vorota.jpg'}
        route_data['timeTable'].append(route_chunk)
        route_timestamp += timestamp_shift
    return route_data


def recommend_routes(user_data: dict) -> dict:
    user_fb = fb.Facebook(access_token=user_data['access_token'],
                          user_id=user_data['user_id'])
    routes_data = {}
    return parse_routes(routes_data)


def parse_routes(routes_data: dict) -> dict:
    return {'routes': [{'image': 'https://s0.rbk.ru/v6_top_pics/media/img/7/59/755060771782597.jpg',
                        'cityName': 'San Francisco',
                        'timeTable': [{'time': '1581242400',
                                       'place': 'Golden Gate Bridge',
                                       'placeImage': 'https://top10.travel/wp-content/uploads/2017/02/most-zolotye-vorota.jpg'},
                                      {'time': '1581242400',
                                       'place': 'Golden Gate Bridge',
                                       'placeImage': 'https://top10.travel/wp-content/uploads/2017/02/most-zolotye-vorota.jpg'},
                                      {'time': '1581242400',
                                       'place': 'Golden Gate Bridge',
                                       'placeImage': 'https://top10.travel/wp-content/uploads/2017/02/most-zolotye-vorota.jpg'}]}]}
