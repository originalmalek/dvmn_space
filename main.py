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
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, filename + file_format), 'wb') as file:
        file.write(response.content)
    print('pic downloaded')


def fetch_spacex_last_launch():
    api_url = 'https://api.spacexdata.com/v4/launches/latest'
    response = requests.get(api_url).json()

    links = response['links']['flickr']['original']
    for counter, link in enumerate(links, 1):
        get_picture_from_url(link, 'space' + str(counter), get_file_format(link))


def get_file_format(link):
    file_format = link.split('.')[-1]
    return '.' + file_format


def fetch_hubble(id):
    url = f'http://hubblesite.org/api/v3/image/{id}'
    response = requests.get(url).json()

    links = response['image_files']
    link = 'https:' + links[-1]['file_url']
    get_picture_from_url(link, 'hubble_' + str(id),  get_file_format(link))


def get_ids_hubble_collections(url):
    response = requests.get(url).json()

    for i in range(len(response)):
        fetch_hubble(response[i]['id'])


def resize_photos():
    file_names = os.listdir(path=os.path.join('images'))
    directory = 'images_resized'

    if not os.path.exists(directory):
        os.makedirs(directory)

    for file_name in file_names:
        image = Image.open(os.path.join('images', file_name)).convert('RGB')
        sizes = image.size

        if sizes[0] > sizes[1] and sizes[0] > 1080:
            image.thumbnail((1075, sizes[1]))
        elif sizes[1] > sizes[0] and sizes[1] > 1080:
            image.thumbnail((sizes[0], 1075 ))
        else:
            pass

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
    collection_name = 'holiday_cards'
    fetch_spacex_last_launch()
    get_ids_hubble_collections(f'http://hubblesite.org/api/v3/images?collection_name={collection_name}')
    post_photo_instagram()


if __name__ == '__main__':
    main()