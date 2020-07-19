import os
import requests

from dotenv import load_dotenv
from instabot import Bot
from PIL import Image
from random import randint
from time import sleep


def get_picture_from_url(url, filename, file_format):
    filename = filename

    response = requests.get(url)
    response.raise_for_status()

    directory = 'images'
    os.makedirs(directory, exist_ok=True)

    with open(os.path.join(directory, filename + file_format), 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    api_url = 'https://api.spacexdata.com/v4/launches/latest'
    response = requests.get(api_url).json()

    links = response['links']['flickr']['original']
    for counter, link in enumerate(links, 1):
        get_picture_from_url(link, 'space' + str(counter), get_file_format(link))


def get_file_format(link):
    return os.path.splitext(link)[-1]


def fetch_hubble(id):
    url = f'http://hubblesite.org/api/v3/image/{id}'
    response = requests.get(url).json()

    links = response['image_files']
    link = 'https:' + links[-1]['file_url']
    get_picture_from_url(link, 'hubble_' + str(id),  get_file_format(link))


def get_ids_hubble_collections():
    collection_name = 'holiday_cards'
    url = f'http://hubblesite.org/api/v3/images?collection_name={collection_name}'
    response = requests.get(url).json()

    for image_info in response:
        fetch_hubble(image_info['id'])


def resize_photos():
    file_names = os.listdir(path=os.path.join('images'))
    directory = 'images_resized'

    os.makedirs(directory, exist_ok=True)

    for file_name in file_names:
        image = Image.open(os.path.join('images', file_name)).convert('RGB')
        image.thumbnail((1075, 1075))
        image.save(os.path.join(directory, file_name.split('.')[0] + '.jpg'), format='JPEG', )


def post_photo_instagram():
    load_dotenv()
    username_insta = os.getenv('USERNAME_INSTA')
    pass_insta = os.getenv('PASS_INSTA')

    file_names = os.listdir(path=os.path.join('images_resized'))

    bot = Bot()
    bot.login(username=username_insta, password=pass_insta)

    for file_name in file_names:
        bot.upload_photo(os.path.join('images_resized', file_name), caption="My last photo is amazing")
        sleep(randint(60, 120))
    bot.logout()


def main():
    fetch_spacex_last_launch()
    get_ids_hubble_collections()
    post_photo_instagram()


if __name__ == '__main__':
    main()
