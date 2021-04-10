import fire
import urllib
import os
import requests
import ctypes
import logging
from time import sleep
from PIL import Image
from asyncio import Queue
from pathlib import Path
from urllib.parse import urljoin

API_LINK = urljoin("https://api.unsplash.com",
                   "photos/random/?client_id=gkuFSia_Rch2GYRK67s8gIfvzRaM73nbnIuYij986Nw")
storage_path = Path.home() \
                   / 'AppData' / 'Roaming' / 'JetBrains' / 'PyCharmCE2020.1' / 'scratches' / 'Images4Desktop'
leave = 0

logging.basicConfig(level=logging.INFO)


def desktop_changer(changes_num: int = 5):

    global leave
    photos_queue = Queue(maxsize=changes_num)
    logging.basicConfig(level=logging.INFO)

    logging.info("I will now go fetch %s random pictures then set them as your background", changes_num)

    while leave != "Yes":

        for j in range(changes_num):
            jason_data = requests.get(API_LINK).json()
            urllib.request.urlretrieve(
                jason_data['urls']['full'], "BackGround")
            background = Image.open("Background")
            random_photo = storage_path.joinpath(f'CBG{j}.jpg')
            background.save(random_photo)
            photos_queue.put_nowait(random_photo)
            logging.info(f"Loading background number %s"
                         f" when i reach %s the magic will begin!",
                         photos_queue.qsize(), changes_num)

        sleep(0.5)
        logging.info("Starting the Desktop change")
        sleep(1)

        if photos_queue.full():

            while not photos_queue.empty():
                logging.info("Current BG is number %s in line",
                             photos_queue.qsize())
                ctypes.windll.user32.SystemParametersInfoW(
                    20, 0, str(photos_queue.get_nowait()), 0)
                sleep(2)

        logging.info("That's all for now , i shall now delete the backgrounds from your memory")
        for n in range(changes_num):
            os.remove(storage_path.joinpath(f"CBG{n}.jpg"))

        leave = input("Would you like to quit ? Type Yes if so , Enter anything else if you wanna go again!")

    else:
        logging.info("Thanks for using me!")
        sleep(2)


if __name__ == "__main__":
    logging.info("Hello ! Welcome to my background changer.")

    fire.Fire(desktop_changer)
