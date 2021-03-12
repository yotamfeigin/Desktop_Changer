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

logging.basicConfig(level=logging.INFO)

logging.info("Hello ! Welcome to my background changer.")
sleep(0.5)

num_of_changes = "a"
while type(num_of_changes) != int:
    try:
        num_of_changes = int(input("How many backgrounds would you like me to fetch?"))
    except ValueError:
        logging.error("Please enter a integer input only")


def desktop_changer():
    photos_queue = Queue(maxsize=num_of_changes)
    logging.basicConfig(level=logging.INFO)

    logging.info("I will now go fetch " + str(num_of_changes)
                 + " random pictures then set them as your background")

    leave = 0
    storage_path = Path.home() \
                   / 'AppData' / 'Roaming' / 'JetBrains' / 'PyCharmCE2020.1' / 'scratches' / 'Images4Desktop'

    while leave != "Yes":

        for j in range(num_of_changes):
            jason_data = requests.get(API_LINK).json()
            urllib.request.urlretrieve(
                jason_data['urls']['full'], "BackGround")
            background = Image.open("Background")
            background.save(storage_path.joinpath(f'CBG{j}.jpg'))
            random_photo = storage_path.joinpath(f'CBG{j}.jpg')
            photos_queue.put_nowait(random_photo)
            logging.info(f"Loading background number {photos_queue.qsize()}"
                         f" when i reach {num_of_changes} the magic will begin!")
        sleep(0.5)
        logging.info("Starting the Desktop change")
        sleep(1)

        if photos_queue.full():

            while not photos_queue.empty():
                logging.info(f"Current BG is number {photos_queue.qsize()} in line")
                ctypes.windll.user32.SystemParametersInfoW(
                    20, 0, str(photos_queue.get_nowait()), 0)
                sleep(2)

        logging.info("That's all for now , i shall now delete the backgrounds from your memory")
        for n in range(num_of_changes):
            os.remove(storage_path.joinpath(f"CBG{n}.jpg"))

        leave = input("Would you like to quit ? Type Yes if so , Enter anything else if you wanna go again!")
    else:
        logging.info("Thanks for using me!")
        sleep(2)


if __name__ == "__main__":
    desktop_changer()
