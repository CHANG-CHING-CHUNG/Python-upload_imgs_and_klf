import os
from os import walk
from os.path import splitext, basename
from dotenv import load_dotenv
from db_class import db
import uuid
import re
import datetime
from PIL import Image
load_dotenv()

class uploadImgAndKlf:
  def __init__(self, images_klf_path, save_image_klf_path):
        self.images_klf_path = images_klf_path
        self.save_image_klf_path = save_image_klf_path

  def upload_imgs_and_klf(self,images_klf_path):
    klf_list, imgs_list = self.get_all_filenames(images_klf_path)
    uuid_batch_number = str(uuid.uuid1())
    current_time = datetime.datetime.now()
    upload_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # print(self.loop_klf_list(images_klf_path, klf_list, uuid_batch_number, upload_time))
    self.loop_imgs_list(images_klf_path, imgs_list, uuid_batch_number, upload_time)
    return

  def loop_klf_list(self,images_klf_path, klf_list, uuid_batch_number, upload_time):
    returned_uuid = None
    for klf in klf_list:
      klf_bytes = open(images_klf_path + klf,"rb").read()
      klf_filenmame,klf_extension = splitext(klf)
      returned_uuid = self.upload_klf_to_db(uuid_batch_number, klf_filenmame, klf_bytes, klf_extension, upload_time)
    return returned_uuid

  def loop_imgs_list(self, images_klf_path, imgs_list, uuid_batch_number, upload_time):
    print(imgs_list)
    print(uuid_batch_number)
    print(upload_time)
    for img in imgs_list:
      img_path = images_klf_path+img
      img = Image.open(img_path)
      img_name, img_extension = splitext(basename(img.filename))
      print(img_name)
      print(img_extension)

    return

  def upload_img_to_db(self,uuid_batch_number, img_name, img_data, img_extension, upload_time):

    return

  def upload_klf_to_db(self,uuid_batch_number, klf_filenmame, klf_bytes, klf_extension, upload_time):
    insert_klf_query = """insert into web_server_klf_store(klf_uuid, klf_filename, klf_data, klf_mine_type, klf_upload_time) 
                          values(%s, %s, %s, %s, %s) returning klf_uuid;"""
    query_var = (uuid_batch_number, klf_filenmame, db.Binary(klf_bytes), klf_extension, upload_time,)
    db.execute_query(insert_klf_query, query_var)
    returned_uuid = db.fetchone()[0]
    return returned_uuid

  def download_imgs_and_klf(self,save_image_klf_path, uuid_batch_number, upload_time):
    klf_list_from_db = self.download_klf_from_db(uuid_batch_number, upload_time)[0]
    klf_name = klf_list_from_db[2]
    klf_extension = klf_list_from_db[4]
    klf_bytes = klf_list_from_db[3]
    self.save_klf_to_target_dir(save_image_klf_path, klf_name,klf_extension, klf_bytes)
    return

  def download_klf_from_db(self,uuid_batch_number, upload_time):
    select_klf_query = """select * from web_server_klf_store 
                          where klf_uuid = %s and klf_upload_time = %s;"""
    query_var = (uuid_batch_number, upload_time,)
    db.execute_query(select_klf_query, query_var)
    result = db.fetchall()
    return result
  
  def save_klf_to_target_dir(self,directory_path, klf_name,klf_extension, klf_bytes):
    target_dir_path = directory_path + klf_name + klf_extension
    klf_bytes = bytes(klf_bytes).decode('UTF-8')
    f = open(target_dir_path,"w")
    f.write(klf_bytes)
    return

  def get_all_filenames(self, directory_path):
    imgs_list = []
    klf_list = []
    filenames_list = []
    for (dirpath, dirnames, filenames) in walk(directory_path):
        filenames_list.extend(filenames)
    for file in filenames_list:
        if len(re.findall(".txt",file)):
          klf_list.append(file)
        else:
          imgs_list.append(file)
    return [klf_list,imgs_list]

images_klf_path  = os.getenv("IMAGES_KLF_PATH")
save_image_klf_path  = os.getenv("SAVE_IMAGE_KLF_PATH")


upload_img_and_klf = uploadImgAndKlf(images_klf_path,save_image_klf_path)

upload_img_and_klf.upload_imgs_and_klf(images_klf_path)

# upload_img_and_klf.download_imgs_and_klf(save_image_klf_path ,"df7d1545-d3f6-11eb-a356-a8a15963b507","2021-06-23 15:44:42+08")