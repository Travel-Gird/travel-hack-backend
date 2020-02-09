import facebook

import db
import utils
import config


def create_fb_user(user_id: str,
                   access_token: str,
                   budget: int,
                   activity: int):
    user_fb = Facebook(user_id=user_id,
                       access_token=access_token)
    user_fb_data = user_fb.get_user_info()
    if user_fb_data is not None:
        db.save_user_to_db(user_fb_id=user_fb_data['id'],
                           age=user_fb_data['age'],
                           gender=user_fb_data['gender'],
                           location=user_fb_data['location'],
                           budget=config.BUDGETS[budget],
                           activity=config.ACTIVITIES[activity])


class Facebook:
    fields = ['birthday',
              'gender',
              'location']

    def __init__(self, access_token: str, user_id: str):
        self.graph = facebook.GraphAPI(access_token=access_token)
        self.user_id = user_id

    def get_user_info(self) -> dict or None:
        fields = ','.join(field for field in self.fields)
        user_fb_object = self.graph.get_object(id='me',
                                               fields=fields)
        user_data = {
            'age': utils.birthday_to_age(user_fb_object['birthday']) if 'birthday' in user_fb_object else 20,
            'gender': (1 if user_fb_object['gender'] == 'male' else 0) if 'gender' in user_fb_object else 1,
            'location': user_fb_object['location']['id'] if 'location' in user_fb_object else '115085015172389',
            'id': user_fb_object['id']
        }
        return user_data

    def get_user_full_info(self) -> dict:
        posts = self.get_posts()
        images = self.get_images_from_posts(posts)
        return {'id': self.user_id,
                'posts': posts,
                'images': images}

    def get_posts(self) -> list:
        posts = self.graph.get_connections(self.user_id, 'posts')
        return posts['data']

    def get_images_from_posts(self, posts: list) -> list:
        image_ids = [post['id'] for post in posts]
        images_data = self.graph.get_objects(ids=image_ids,
                                             fields='full_picture')
        images_urls = [image_data['full_picture']
                       for _, image_data in images_data.items()
                       if 'full_picture' in image_data]
        return images_urls


if __name__ == '__main__':
    fb = Facebook(access_token=config.TEST_USER_FB_ACCESS_TOKEN,
                  user_id=config.TEST_USER_FB_ID)
    fb_posts = fb.get_posts()
    print(fb_posts)
    fb_images = fb.get_images_from_posts(fb_posts)
    print(fb_images)
    fb_user_info = fb.get_user_info()
    print('\n')
    print('User info')
    print(fb_user_info)
