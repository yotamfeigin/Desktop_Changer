#import fire
import urllib
import os
import requests
import ctypes
import logging
import asyncio
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



async def remover(n):
    await asyncio.sleep(1)
    for i in range(n):
        os.remove(storage_path.joinpath(f"CBG{i}.jpg"))

async def setter(waited):
    global photos_queue
    print(photos_queue.full())
    if photos_queue.full():
        while not photos_queue.empty():
            logging.info("Current BG is number %s in line",
                         photos_queue.qsize())
            (ctypes.windll.user32.SystemParametersInfoW(
                20, 0, waited, 0))
            await asyncio.sleep(1.5)


def queue():
    global leave
    logging.info("I will now go fetch %s random pictures then set them as your background", changes_num)

    while not photos_queue.full():

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

async def main():

    queue()
    print(photos_queue.full())
    task1 = asyncio.create_task(setter(str(photos_queue.get_nowait())))
    task2 = asyncio.create_task(remover(changes_num))
    await asyncio.gather(
        task1,task2

    )


if __name__ == "__main__":
    changes_num: int = 5
    photos_queue = Queue(maxsize=changes_num)
    logging.basicConfig(level=logging.INFO)
    logging.info("Hello ! Welcome to my background changer.")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
   # fire.Fire(desktop_changer)
