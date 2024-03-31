import requests
import simplejson as json
from progress.bar import IncrementalBar


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
        print(response.json())
        result = {}
        json_data = []
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
                size = 'w'
            elif 'z' in dict_foto:
                result[likes] = dict_foto['z']
                size = 'z'
            elif 'y' in dict_foto:
                result[likes] = dict_foto['y']
                size = 'y'
            elif 'r' in dict_foto:
                result[likes] = dict_foto['r']
                size = 'r'
            elif 'q' in dict_foto:
                result[likes] = dict_foto['q']
                size = 'q'
            json_data.append({'file_name': f'{likes}.jpg', 'size': size})
        with open('new.json', 'w') as f:
            json.dump(json_data, f)
        return result


class Ya:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'{self.token}'
        }

    def newfolder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'cloud_api': 'disk.write', 'path': 'ImageVK'}
        requests.put(url, headers={**self.headers}, params={**params})

    def uploadfoto(self, dict_fotos):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        # i = 0
        bar = IncrementalBar('Выполнено', max=len(dict_fotos))
        bar.next(0)
        for foto in dict_fotos:
            requests.post(url, headers=self.headers,
                          params={'url': dict_fotos[foto], 'path': f'ImageVK/{foto}.jpg'})
            bar.next()
            # i += 1
            # print(f'выполнено {round(i * 100 / len(dict_fotos), 1)}%')
        bar.finish()

        responce = requests.get(url, headers=self.headers,
                                params={'path': 'ImageVK/foto.json'}
                                )
        url_for_up = responce.json()['href']
        with open('new.json', 'r') as f:
            requests.put(url_for_up, files={'file': f})


with open('vk.txt', 'r') as f:
    vk_token = str(f.readline())
print(vk_token)
user_id = str(input('Введите id vk'))
vk = VK(vk_token, user_id)
with open('ya.txt', 'r') as f:
    ya_token = str(f.readline())
ya = Ya(ya_token)
ya.newfolder()
ya.uploadfoto(vk.get_photo())
