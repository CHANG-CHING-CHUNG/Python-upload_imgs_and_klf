import os
from current_version_copy import uploadImgAndKlf
import logging
import time
import datetime
from dotenv import load_dotenv
load_dotenv()

TRAIN_IMG_PATH = os.getenv('TRAIN_IMG_PATH')
SAVE_IMAGE_KLF_PATH = os.getenv('SAVE_IMAGE_KLF_PATH')
upload_img_and_klf = uploadImgAndKlf()

returned_uuid_and_upload_time = upload_img_and_klf.upload_imgs(TRAIN_IMG_PATH)

current_date = datetime.datetime.now()
current_date = current_date.strftime("%Y-%m-%d")

logging.basicConfig(filename=f"{current_date}-before-img-download.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)
start_time = time.time()
logging.info('優化前圖片下載速度測試開始')

upload_img_and_klf.download_imgs_wrapper_for_predict(SAVE_IMAGE_KLF_PATH, returned_uuid_and_upload_time, False, True)

end_time = time.time()
elapsed_time = end_time - start_time
logging.info('優化前圖片下載速度測試結束')
logging.info(f'下載花費時間: {elapsed_time}')
logging.info('\n')


logging.basicConfig(filename=f"{current_date}-after-img-download.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)
start_time = time.time()
logging.info('優化後圖片下載速度測試開始')

upload_img_and_klf.download_imgs_wrapper_for_train(SAVE_IMAGE_KLF_PATH, returned_uuid_and_upload_time, False)

end_time = time.time()
elapsed_time = end_time - start_time
logging.info('優化後圖片下載速度測試結束')
logging.info(f'下載花費時間: {elapsed_time}')
logging.info('\n')
