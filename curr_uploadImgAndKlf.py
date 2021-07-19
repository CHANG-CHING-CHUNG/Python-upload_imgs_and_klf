import os
from os import walk
from os.path import splitext, basename
from utils.db_class import db
import uuid
import re
import datetime
from PIL import Image
import io
from settings.config import get_config
import pathlib
import shutil



class uploadImgAndKlf:
  def upload_predict_klf_and_img(self, images_klf_path,klf_list,imgs_list):
    # klf_list, imgs_list = self.get_all_filenames(images_klf_path)
    uuid_batch_number = str(uuid.uuid1())
    current_time = datetime.datetime.now()
    upload_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    returned__klf_uuid = self.loop_klf_list(images_klf_path, klf_list, uuid_batch_number, upload_time)
    returned_img_uuid = self.loop_imgs_list(images_klf_path, imgs_list, uuid_batch_number, upload_time)
    if returned__klf_uuid != None and returned_img_uuid != None and returned__klf_uuid == returned_img_uuid:
      return [returned__klf_uuid, upload_time]
    else:
      return []

  def upload_imgs_and_klf(self, images_klf_path):
    klf_list, imgs_list = self.get_all_filenames(images_klf_path)
    uuid_batch_number = str(uuid.uuid1())
    current_time = datetime.datetime.now()
    upload_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    returned__klf_uuid = self.loop_klf_list(images_klf_path, klf_list, uuid_batch_number, upload_time)
    returned_img_uuid = self.loop_imgs_list(images_klf_path, imgs_list, uuid_batch_number, upload_time)
    if returned__klf_uuid != None and returned_img_uuid != None and returned__klf_uuid == returned_img_uuid:
      return [returned__klf_uuid, upload_time]
    else:
      return []

  def upload_klf_by_name_list(self,input_dir_path, klf_list):
    uuid_batch_number = str(uuid.uuid1())
    current_time = datetime.datetime.now()
    upload_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    returned__klf_uuid = self.loop_klf_list(input_dir_path, klf_list, uuid_batch_number, upload_time)
    # returned_img_uuid = self.loop_imgs_list(images_klf_path, imgs_list, uuid_batch_number, upload_time)
    if returned__klf_uuid != None :
      return [returned__klf_uuid, upload_time]
    else:
      return []


  def upload_data_cleaning_imgs_by_lisy(self, train_img_path, classes_list ):
    imgs_list = list()
    for train_class in classes_list:
      img_path =  os.path.join(train_img_path,train_class)
      imgs_list = self.get_all_img_filenames(img_path) + imgs_list

    uuid_batch_number = str(uuid.uuid1())
    current_time = datetime.datetime.now()
    upload_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    returned_img_uuid = self.loop_imgs_list_for_training(train_img_path, imgs_list, uuid_batch_number, upload_time)
    if returned_img_uuid != None:
      return [returned_img_uuid, upload_time]
    else:
      return []

  def upload_imgs(self, train_img_path):
    imgs_list = self.get_all_img_filenames(train_img_path)
    uuid_batch_number = str(uuid.uuid1())
    current_time = datetime.datetime.now()
    upload_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    returned_img_uuid = self.loop_imgs_list_for_training(train_img_path, imgs_list, uuid_batch_number, upload_time)
    if returned_img_uuid != None:
      return [returned_img_uuid, upload_time]
    else:
      return []

  def upload_data_cleaning_imgs(self, train_img_path):
    imgs_list = self.get_all_img_filenames(train_img_path)
    uuid_batch_number = str(uuid.uuid1())
    current_time = datetime.datetime.now()
    upload_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    returned_img_uuid = self.loop_imgs_list_for_data_cleaning(train_img_path, imgs_list, uuid_batch_number, upload_time)
    if returned_img_uuid != None:
      return [returned_img_uuid, upload_time]
    else:
      return []

  def loop_klf_list(self, images_klf_path, klf_list, uuid_batch_number, upload_time):
    returned_uuid = None
    try:
      if klf_list:
        for klf in klf_list:
          klf_bytes = open(os.path.join(images_klf_path, klf), "rb").read()
          klf_filenmame, klf_extension = splitext(klf)
          self.upload_klf_to_db(uuid_batch_number, klf_filenmame, klf_bytes, klf_extension, upload_time)
        db.commit()
        returned_uuid = db.fetchone()[0]
    except Exception as e:
      db.conn_rollback()
      print("db error: {}".format(e))
    return returned_uuid

  def loop_imgs_list(self, images_klf_path, imgs_list, uuid_batch_number, upload_time):
    returned_uuid = None
    try:
      if imgs_list :
        for img in imgs_list:
          img_path = os.path.join(images_klf_path,img)
          img = Image.open(img_path)
          img_name, img_extension = splitext(basename(img.filename))
          img_bytes = self.convert_image_to_bytes(img)
          self.upload_img_to_db(uuid_batch_number, img_name, img_bytes, img_extension, upload_time)
        db.commit()
        returned_uuid = db.fetchone()[0]
    except Exception as e:
      db.conn_rollback()
      print("db error: {}".format(e))
    return returned_uuid

  def loop_imgs_list_for_training(self, images_klf_path, imgs_list, uuid_batch_number, upload_time):
    returned_uuid = None

    try:
      if imgs_list:
        for img_dict in imgs_list:
          img_path = img_dict["path"] + img_dict["img_name"]
          folder_name = img_dict["path"].split("/")[-2]
          img = Image.open(img_path)
          img_name, img_extension = splitext(basename(img.filename))
          img_bytes = self.convert_image_to_bytes(img)
          self.upload_img_to_db(uuid_batch_number, img_name, img_bytes, img_extension, upload_time, folder_name)
        db.commit()
        returned_uuid = db.fetchone()[0]
    except Exception as e:
      db.conn_rollback()
      print("db error: {}".format(e))
    return returned_uuid


  def loop_imgs_list_for_data_cleaning(self, images_klf_path, imgs_list, uuid_batch_number, upload_time):
    returned_uuid = None
    try:
      if imgs_list:
        for img_dict in imgs_list:
          img_path = img_dict["path"] + img_dict["img_name"]
          folder_name = os.path.join( img_dict["path"].split("/")[-3],  img_dict["path"].split("/")[-2])
          img = Image.open(img_path)
          img_name, img_extension = splitext(basename(img.filename))
          img_bytes = self.convert_image_to_bytes(img)
          self.upload_img_to_db(uuid_batch_number, img_name, img_bytes, img_extension, upload_time, folder_name)
        db.commit()
        returned_uuid = db.fetchone()[0]
    except Exception as e:
      db.conn_rollback()
      print("db error: {}".format(e))
    return returned_uuid

  def upload_img_to_db(self, uuid_batch_number, img_name, img_data, img_extension, upload_time, img_path=None):
    insert_query = """insert into web_server_img_store(img_uuid, img_name, img_data, img_mine_type, img_upload_time) 
                      VALUES(%s,%s,%s,%s,%s) RETURNING img_uuid"""
    query_var = (uuid_batch_number, img_name, img_data, img_extension, upload_time)
    if img_path:
      insert_query = """insert into web_server_img_store(img_uuid, img_name, img_data, img_mine_type, img_upload_time, img_path) 
                    VALUES(%s,%s,%s,%s,%s,%s) RETURNING img_uuid"""
      query_var = (uuid_batch_number, img_name, img_data, img_extension, upload_time, img_path)
    db.execute_query_without_commit(insert_query, query_var)
    # returned_id = db.fetchone()[0]
    return

  def upload_klf_to_db(self, uuid_batch_number, klf_filenmame, klf_bytes, klf_extension, upload_time):
    insert_klf_query = """insert into web_server_klf_store(klf_uuid, klf_filename, klf_data, klf_mine_type, klf_upload_time) 
                          values(%s, %s, %s, %s, %s) returning klf_uuid;"""
    query_var = (uuid_batch_number, klf_filenmame, klf_bytes, klf_extension, upload_time,)
    db.execute_query_without_commit(insert_klf_query, query_var)
    # returned_uuid = db.fetchone()[0]
    return

  def download_imgs_and_klf(self, save_image_klf_path, uuid_batch_number, upload_time, img_is_deleted):
    klf_list_from_db = self.download_klf_from_db(uuid_batch_number, upload_time)
    for klf in klf_list_from_db:
      klf_name = klf[0]
      klf_extension = klf[2]
      klf_bytes = klf[1]
      self.save_klf_to_target_dir(save_image_klf_path, klf_name, klf_extension, klf_bytes)

    img_list_from_db = self.download_img_from_db(uuid_batch_number, upload_time, img_is_deleted)
    for img in img_list_from_db:
      img_name = img[0]
      img_bytes = img[1]
      img_extension = img[2]
      self.save_img_to_target_dir(save_image_klf_path, img_name, img_extension, img_bytes)
    return

  def download_img_list_from_db(self,uuid_batch_number, upload_time, is_deleted=False):
    select_img_query = """select img_name, img_mine_type, img_path from web_server_img_store 
                          where img_uuid = %s 
                          and img_upload_time = %s
                          and img_is_deleted = %s;"""
    query_var = (uuid_batch_number, upload_time, is_deleted,)
    db.execute_query(select_img_query, query_var)
    result = db.fetchall()
    result_list = []
    for img in result:
      img_dict = {
        "path":img[2],
        "img_name":img[0]+img[1]
      }
      result_list.append(img_dict)
    return result_list

  def get_local_img_list(self, save_image_path):
    dirpath_list = []
    for (dirpath, dirnames, filenames) in walk(save_image_path):
        for filename in filenames:
          img_dict = {
            "path":dirpath,
            "img_name":filename
          }
          dirpath_list.append(img_dict)
    return dirpath_list

  def filtered_imgs(self,img_list_without_bytea, local_img_list, condition_str):
    condition_list = ["not in db list", "repeated imgs"]
    db_img_list_len = len(img_list_without_bytea)
    local_img_list_len = len(local_img_list)

    filtered_img_list = []

    for img in local_img_list:
      is_valid = False
      for img_db in img_list_without_bytea:
        if img['img_name'] == img_db['img_name']:
          is_valid = True
          break
      if condition_str == condition_list[0] and not is_valid:
          filtered_img_list.append(img)
      elif condition_str == condition_list[1] and is_valid:
          filtered_img_list.append(img)

    return filtered_img_list

  def clear_imgs_not_exist_in_db(self,img_list_without_bytea, local_img_list):
    local_img_to_remove = self.filtered_imgs(img_list_without_bytea, local_img_list, "not in db list")
    for img in local_img_to_remove:
      img_path = os.path.join(img["path"],img["img_name"])
      if os.path.exists(img_path):
        os.remove(img_path)
      else:
        print("Can not delete the file as it doesn't exists")
    return

  def check_repeated_imgs(self,img, repeated_img_list):
    for repeated_img in repeated_img_list:
      if img["img_name"] == repeated_img["img_name"]:
        return True
    return False

  def remove_repeated_imgs_from_list(self,img_list_without_bytea, local_img_list):
    repeated_img_list = self.filtered_imgs(img_list_without_bytea, local_img_list, "repeated imgs")
    new_img_list = []
    for img in img_list_without_bytea:
      is_repeated = self.check_repeated_imgs(img, repeated_img_list)
      if not is_repeated:
        new_img_list.append(img)
    
    return new_img_list

  def download_klf_and_backup(self, save_path, output_path, info_list):
    uuid_batch_number, upload_time = info_list
    klf_list_from_db = self.download_klf_from_db(uuid_batch_number, upload_time)
    for klf in klf_list_from_db:
      klf_name = klf[0]
      klf_extension = klf[2]
      klf_bytes = klf[1]
      self.save_klf_to_target_dir(save_path, klf_name, klf_extension, klf_bytes)

    for klf in klf_list_from_db:
      klf_name = klf[0]
      klf_extension = klf[2]
      klf_backup_path = os.path.join(save_path, klf_name + klf_extension)
      output_name = klf_name.split("$$")[-1]
      klf_output_path = os.path.join(output_path, output_name + klf_extension)
      shutil.copyfile(klf_backup_path, klf_output_path)

    return

  def download_imgs(self, save_image_path, uuid_batch_number, upload_time, img_is_deleted, has_path=False):
    img_list_from_db = self.download_img_from_db_for_predict(uuid_batch_number, upload_time, img_is_deleted, has_path)
    for img in img_list_from_db:
      img_name = img[0]
      img_bytes = img[1]
      img_extension = img[2]
      if has_path:
        img_path = img[3]
        self.save_img_to_target_dir(save_image_path, img_name, img_extension, img_bytes, img_path)
      else:
        self.save_img_to_target_dir(save_image_path, img_name, img_extension, img_bytes)
    return

  def download_imgs_for_train(self,save_image_path, uuid_batch_number, upload_time,img_is_deleted):
    img_list_without_bytea = self.download_img_list_from_db(uuid_batch_number, upload_time,img_is_deleted)
    local_img_list = self.get_local_img_list(save_image_path)
    self.clear_imgs_not_exist_in_db(img_list_without_bytea, local_img_list)
    new_img_list = self.remove_repeated_imgs_from_list(img_list_without_bytea, local_img_list)
    new_img_list = tuple(map(lambda img: img["img_name"].split(".")[0], new_img_list))
    if not new_img_list:
      return
    img_list_from_db = self.download_img_from_db_by_list(uuid_batch_number, upload_time, new_img_list, img_is_deleted)
    for img in img_list_from_db:
      img_name = img[0]
      img_bytes = img[1]
      img_extension = img[2]
      img_path = img[3]
      self.save_img_to_target_dir(save_image_path, img_name, img_extension, img_bytes, img_path)
    return

  def rm_klf(self,path,info_list):
    uuid_batch_number, upload_time = info_list
    klf_list_from_db = self.download_klf_from_db(uuid_batch_number, upload_time)
    for klf in klf_list_from_db:
      klf_name = klf[0]
      klf_extension = klf[2]
      target_path = os.path.join(path, klf_name + klf_extension)
      os.remove(target_path)

  def rm_img(self,path,info_list):
    uuid_batch_number, upload_time = info_list
    img_list_from_db = self.download_img_from_db(uuid_batch_number, upload_time)
    for img in img_list_from_db:
      img_name = img[0]
      img_extension = img[2]
      target_path = os.path.join(path, img_name + img_extension)
      os.remove(target_path)
    pass

  def download_klf_from_db(self, uuid_batch_number, upload_time):
    select_klf_query = """select klf_filename, klf_data, klf_mine_type from web_server_klf_store 
                          where klf_uuid = %s and klf_upload_time = %s;"""
    query_var = (uuid_batch_number, upload_time,)
    db.execute_query(select_klf_query, query_var)
    result = db.fetchall()
    return result

  def download_img_from_db_for_predict(self, uuid_batch_number, upload_time, is_deleted=False, has_path=False):
    select_img_query = """select img_name, img_data, img_mine_type from web_server_img_store 
                          where img_uuid = %s 
                          and img_upload_time = %s
                          and img_is_deleted = %s;"""
    query_var = (uuid_batch_number, upload_time, is_deleted,)
    if has_path:
      select_img_query = """select img_name, img_data, img_mine_type, img_path from web_server_img_store 
                          where img_uuid = %s 
                          and img_upload_time = %s
                          and img_is_deleted = %s;"""
    db.execute_query(select_img_query, query_var)
    result = db.fetchall()
    return result

  def download_img_from_db_by_list(self,uuid_batch_number, upload_time, img_list, is_deleted=False):
    select_img_query = """select img_name, img_data, img_mine_type, img_path from web_server_img_store 
                          where img_uuid = %s
                          and img_upload_time = %s
                          and img_is_deleted = %s
                          and img_name
                          in %s;"""
    query_var = (uuid_batch_number, upload_time, is_deleted,img_list)
    db.execute_query(select_img_query, query_var)
    result = db.fetchall()
    return result

  def save_img_to_target_dir(self, directory_path, img_name, img_extension, img_bytes, img_path=None):
    target_dir_path = os.path.join(directory_path , img_name + img_extension)
    if img_path:
      target_dir_full_path = os.path.join(directory_path, img_path)
      path = pathlib.Path(target_dir_full_path)
      path.mkdir(parents=True, exist_ok=True)
      target_dir_path =  os.path.join(target_dir_full_path , img_name + img_extension)
    img = self.read_image_from_bytes(img_name, img_bytes)
    img.save(target_dir_path, format=img.format)
    return

  def read_image_from_bytes(self, img_name, img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    img.filename = img_name
    return img

  def save_klf_to_target_dir(self, directory_path, klf_name, klf_extension, klf_bytes):
    target_dir_path = os.path.join(directory_path , klf_name + klf_extension)
    klf_bytes = bytes(klf_bytes).decode('UTF-8')
    f = open(target_dir_path, "w")
    f.write(klf_bytes)
    return

  def read_image_from_bytes(self, img_name, img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    img.filename = img_name
    return img

  def get_all_filenames(self, directory_path):
    imgs_list = []
    klf_list = []
    filenames_list = []
    for (dirpath, dirnames, filenames) in walk(directory_path):
      filenames_list.extend(filenames)

    for file in filenames_list:
      if len(re.findall(".txt", file)):
        klf_list.append(file)
      else:
        imgs_list.append(file)
    return [klf_list, imgs_list]

  def get_all_img_filenames(self, directory_path):
    imgs_list = []

    for (dirpath, dirnames, filenames) in walk(directory_path):
      if len(filenames) >= 1:
        for file in filenames:
          if len(re.findall(".jpeg|.jpg", file)):
            path_img_dict = {
              "path": dirpath + "/",
              "img_name": file
            }
            imgs_list.append(path_img_dict)

    return imgs_list

  def convert_image_to_bytes(self, img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

  def download_imgs_and_klf_wrapper(self, save_image_klf_path, returned_uuid_and_upload_time_list, is_deleted):
    if len(returned_uuid_and_upload_time_list) == 2:
      returned_uuid, upload_time = returned_uuid_and_upload_time_list
      self.download_imgs_and_klf(save_image_klf_path, returned_uuid, upload_time, is_deleted)
      print("download completed")
    else:
      print("Error")


  def download_imgs_wrapper_for_train(self, save_image_path, returned_uuid_and_upload_time_list,is_deleted):
    # is_deleted True download deleted only
    # is_deleted False download not deleted only
    # has_path True save by class dir
    if len(returned_uuid_and_upload_time_list) == 2:
      returned_uuid, upload_time = returned_uuid_and_upload_time_list
      self.download_imgs_for_train(save_image_path ,returned_uuid, upload_time,is_deleted)
      print("download completed")
    else:
      print("Error")

  def download_imgs_wrapper_for_predict(self, save_image_path, returned_uuid_and_upload_time_list,is_deleted,has_path=False):
    if len(returned_uuid_and_upload_time_list) == 2:
      returned_uuid, upload_time = returned_uuid_and_upload_time_list
      self.download_imgs(save_image_path ,returned_uuid, upload_time,is_deleted,has_path)
      print("download completed")
    else:
      print("Error")