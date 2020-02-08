import requests
import facebook


class Facebook:
    def __init__(self, access_token, user_id):
        self.graph = facebook.GraphAPI(access_token=access_token)
        self.user_id = user_id

    def get_posts(self):
        posts = self.graph.get_connections(self.user_id, 'posts')
        return posts['data']

    def _get_images_from_posts(self, posts):
        images = []
        for post in posts:
            image_data = self.graph.get_object(id=post['id'],
                                               fields='full_picture, picture')
            image_url = image_data['data']['full_picture']
            images.append(image_url)

    def _download_image(self, image_url):
        pass

    def _save_images(self, images):
        pass
