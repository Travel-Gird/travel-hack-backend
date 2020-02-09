import random

import fb
import db


def generate_routes(user_id: str, access_token: str, places_data: list) -> list:
    routes = []
    for i in range(0, 5):
        random.shuffle(places_data)
        hours = 8
        route_data = {'image': 'https://www.visittheusa.com/sites/default/files/styles/hero_m_1300x700/public/2017-10/8cd6053c1e15b9054eb0114f63fbc51c.jpeg?itok=q3ghTX27',
                      'cityName': f'Route #{str(i)}',
                      'timeTable': []}
        timeline = []
        for place_id in places_data:
            place_data = db.get_place_from_db(place_id)
            route_chunk = {'time': f'{str(hours)}:00',
                           'place': place_data['title'],
                           'description': place_data['description'],
                           'latitude': str(place_data['latitude']),
                           'longitude': str(place_data['longitude'])}
            route_data['timeTable'].append(route_chunk)
            timeline.append({'place_id': int(place_id),
                             'time': f'{str(hours)}:00'})
            hours += place_data['time_shift'] + 1
        route_id = db.save_route_to_db(timeline)
        route_data.update({'id': str(route_id)})
        routes.append(route_data)
    user_fb = fb.Facebook(user_id=user_id,
                          access_token=access_token)
    user_fb_data = user_fb.get_user_info()
    if user_fb_data is not None:
        db.save_user_to_db(user_fb_data)
    return routes


def rate_route(user_facebook_id: int, route_id: int):
    db.rate_route_in_db(user_facebook_id=user_facebook_id,
                        route_id=route_id)


def recommend_routes(user_data: dict) -> dict:
    user_fb = fb.Facebook(access_token=user_data['access_token'],
                          user_id=user_data['user_id'])
    routes_data = {}
    return routes_data