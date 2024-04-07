import requests
import simplejson as json


class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photo(self, count=5, album_id='profile'):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': album_id,
            'extended': 1
        }
        response = requests.get(url, params={**self.params, **params})
        if response.status_code != 200:
            print('ошибка! status_code отличный от 200')
        result = {}
        for i in range(count):
            likes = str(response.json()['response']['items'][i]['likes']['count'])
            if likes in result:
                likes = likes + str(response.json()['response']['items'][i]['date'])
            foto_sizes = response.json()['response']['items'][i]['sizes']
            dict_foto = {}
            for foto in foto_sizes:
                dict_foto[foto['type']] = foto['url']
            if 'w' in dict_foto:
                result[likes] = dict_foto['w']
            elif 'z' in dict_foto:
                result[likes] = dict_foto['z']
            elif 'y' in dict_foto:
                result[likes] = dict_foto['y']
            elif 'r' in dict_foto:
                result[likes] = dict_foto['r']
            elif 'q' in dict_foto:
                result[likes] = dict_foto['q']
        return result

    def get_json(self, count=5, album_id='profile'):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': album_id,
            'extended': 1
        }
        response = requests.get(url, params={**self.params, **params})
        if response.status_code != 200:
            print('ошибка! status_code отличный от 200')
        json_data = []
        list_likes = []
        for i in range(count):
            likes = str(response.json()['response']['items'][i]['likes']['count'])
            if likes in list_likes:
                likes = likes + str(response.json()['response']['items'][i]['date'])
            list_likes.append(likes)
            foto_sizes = response.json()['response']['items'][i]['sizes']
            list_size = []
            for foto in foto_sizes:
                list_size.append(foto['type'])
            if 'w' in list_size:
                size = 'w'
            elif 'z' in list_size:
                size = 'z'
            elif 'y' in list_size:
                size = 'y'
            elif 'r' in list_size:
                size = 'r'
            elif 'q' in list_size:
                size = 'q'
            json_data.append({'file_name': f'{likes}.jpg', 'size': size})
        with open('new.json', 'w') as f:
            json.dump(json_data, f)
