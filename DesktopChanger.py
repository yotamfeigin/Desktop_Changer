import urllib
from PIL import Image
import asyncio
import os
import requests
import time
import ctypes
import logging
import pathlib
def desktop_changer():
    photos_queue = asyncio.Queue(maxsize=5)
    logging.basicConfig(level=logging.INFO)

    logging.info("Hello ! Welcome to my background changer."
          " \n I will now go fetch 5 random pictures at a time then set them as your background")
    api_link = "https://api.unsplash.com/photos/random/?client_id=gkuFSia_Rch2GYRK67s8gIfvzRaM73nbnIuYij986Nw"
    Quit = 0
    storage_path = pathlib.Path.home().joinpath(
        'AppData','Roaming','JetBrains','PyCharmCE2020.1','scratches','Images4Desktop')
    while Quit != "Yes":

        for j in range(5):
            jason_data = requests.get(api_link).json()
            urllib.request.urlretrieve(
                jason_data['urls']['full'],"BackGround")
            background = Image.open("Background")
            background.save(storage_path.joinpath(f'CBG{j}.jpg'))
            random_photo = storage_path.joinpath(f'CBG{j}.jpg')
            photos_queue.put_nowait(random_photo)
            logging.info(f"Loading background number {photos_queue.qsize()}, when i reach 5 the magic will begin!")
        time.sleep(0.5)
        logging.info("Starting the Desktop change")
        time.sleep(1)

        if photos_queue.full():

            while not photos_queue.empty():
                logging.info(f"Current BG is number {photos_queue.qsize()} in line")
                ctypes.windll.user32.SystemParametersInfoW(
                    20,0,str(photos_queue.get_nowait()),0)
                time.sleep(2)

        logging.info("That's all for now , i shall now delete the backgrounds from your memory")
        for n in range(5):

            os.remove(storage_path.joinpath(f"CBG{n}.jpg"))

        Quit = input("Would you like to quit ? Type Yes if so , Enter anything else if you wanna go again!")
    else:
        logging.info("Thanks for using me!")
        time.sleep(2)

if __name__ == "__main__":
    desktop_changer()
