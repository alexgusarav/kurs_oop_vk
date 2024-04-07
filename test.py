import configparser
import vk
import ya


config = configparser.ConfigParser()
config.read('data.ini')
vk_token = config['VK']['token']
ya_token = config['Ya']['token']
user_id = str(input('Введите id vk '))
vkcom = vk.VK(vk_token, user_id)
vkcom.get_json()
yandex = ya.Ya(ya_token)
yandex.uploadfoto(vkcom.get_photo(), yandex.newfolder())
