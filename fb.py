import requests
import facebook

import db
import config


class Facebook:
    fields = ['education',
              'birthday',
              'favorite_athletes',
              'favorite_teams',
              'gender',
              'hometown',
              'location',
              'sports',
              'posts']

    def __init__(self, access_token: str, user_id: str):
        self.graph = facebook.GraphAPI(access_token=access_token)
        self.user_id = user_id

    def get_user_info(self):
        fields = ','.join(field for field in self.fields)
        user_info = self.graph.get_object(id='me',
                                          fields=fields)
        return user_info

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
