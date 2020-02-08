import fb
import db


def generate_route(places_data: list) -> dict:
    hours = 8
    route_data = {'image': 'https://s0.rbk.ru/v6_top_pics/media/img/7/59/755060771782597.jpg',
                  'cityName': 'San Francisco',
                  'timeTable': []}
    timeline = []
    for place_id in places_data:
        place_data = db.get_place_from_db(place_id)
        route_chunk = {'time': f'{str(hours)}:00',
                       'place': place_data['title'],
                       'description': place_data['description'],
                       'latitude': place_data['latitude'],
                       'longitude': place_data['longitude']}
        route_data['timeTable'].append(route_chunk)
        timeline.append({'place_id': int(place_id),
                         'time': f'{str(hours)}:00'})
        hours += place_data['time_shift'] + 1
    route_id = db.save_route_to_db(timeline)
    route_data.update({'id': str(route_id)})
    return route_data


def rate_route(user_facebook_id: int, route_id: int):
    db.rate_route_in_db(user_facebook_id=user_facebook_id,
                        route_id=route_id)


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
