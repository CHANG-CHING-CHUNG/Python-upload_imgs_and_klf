import asyncio
import websockets
import json
from uploadImgAndKlf import upload_img_and_klf

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

async def download_img_socket(websocket, path):
  save_image_path = "/home/alpha/data/img_klf_save_target/t1/"
  returned_uuid_and_upload_time = await websocket.recv()
  print(f"server received upload result : {returned_uuid_and_upload_time}")

  returned_uuid_and_upload_time_list = json.loads(returned_uuid_and_upload_time)
  upload_img_and_klf.download_imgs_wrapper(save_image_path, returned_uuid_and_upload_time_list, False)


async def download_img__klf_socket(websocket, path):
  save_image_klf_path = "/home/alpha/data/img_klf_save_target/t1/"
  returned_uuid_and_upload_time = await websocket.recv()
  print(f"server received upload result : {returned_uuid_and_upload_time}")

  returned_uuid_and_upload_time_list = json.loads(returned_uuid_and_upload_time)
  upload_img_and_klf.download_imgs_and_klf_wrapper(save_image_klf_path, returned_uuid_and_upload_time_list, False)


start_server = websockets.serve(download_img__klf_socket, "localhost", 8765)
# start_server = websockets.serve(download_img_socket, "localhost", 8765)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()