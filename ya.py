import requests
from progress.bar import IncrementalBar


class Ya:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'{self.token}'
        }

    def newfolder(self):
        folder_name = str(input('Введите название папки на яндекс диске: '))
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'cloud_api': 'disk.write', 'path': f'{folder_name}'}
        while requests.get(url, headers={**self.headers}, params={**params}).status_code != 404:
            folder_name = str(input('папка существует, введите новое имя: '))
            params = {'cloud_api': 'disk.write', 'path': f'{folder_name}'}
        response = requests.put(url, headers={**self.headers}, params={**params})
        if response.status_code != 201:
            print('ошибка! status_code отличный от 201')
        return folder_name

    def uploadfoto(self, dict_fotos, folder_name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        # i = 0
        bar = IncrementalBar('Выполнено', max=len(dict_fotos))
        bar.next(0)
        for foto in dict_fotos:
            response = requests.post(url, headers=self.headers,
                          params={'url': dict_fotos[foto], 'path': f'{folder_name}/{foto}.jpg'})
            if response.status_code != 202:
                print('ошибка! status_code отличный от 202')
            bar.next()
            # i += 1
            # print(f'выполнено {round(i * 100 / len(dict_fotos), 1)}%')
        bar.finish()

        responce = requests.get(url, headers=self.headers,
                                params={'path': f'{folder_name}/foto.json'}
                                )
        if response.status_code != 202:
            print('ошибка! status_code отличный от 202')
        url_for_up = responce.json()['href']
        with open('new.json', 'r') as f:
            requests.put(url_for_up, files={'file': f})
