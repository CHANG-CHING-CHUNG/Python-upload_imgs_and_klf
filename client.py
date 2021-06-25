import asyncio
import websockets
import json
from uploadImgAndKlf import upload_img_and_klf

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

async def upload_img_operation():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # name = input("What's your name? ")
        train_img_path = "/home/alpha/data/train_image_folder/t1/original/"

        print(f"> {train_img_path}")
        result = upload_img_and_klf.upload_imgs(train_img_path)
        await websocket.send(json.dumps(result))
        print(f"client upload result: {json.dumps(result)}")

        result = await websocket.recv()
        print(f"client received result: {result}")

async def upload_img_klf_operation():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # name = input("What's your name? ")
        images_klf_path = "/home/alpha/data/hmls_inline_input_folder/t1/"

        print(f"> {images_klf_path}")
        result = upload_img_and_klf.upload_imgs_and_klf(images_klf_path)
        await websocket.send(json.dumps(result))
        print(f"client upload result: {json.dumps(result)}")

        result = await websocket.recv()
        print(f"client received result: {result}")

asyncio.get_event_loop().run_until_complete(upload_img_klf_operation())