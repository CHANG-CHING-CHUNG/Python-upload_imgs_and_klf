# 鉅芯科技 - 圖片及klf 上傳下載程式用法
###### tags: `鉅芯科技筆記`
## `db_class.py`
連線資料庫用
傳入 HOST, DATABASE, USER 及 PASSWORD 後調用 `connect` 方法即可
![](https://i.imgur.com/zYLGmpV.png)

## `uploadImgAndKlf.py`
### 圖片及 klf 上傳
初始化實例後，調用 `upload_imgs_and_klf` 方法傳入圖片及 klf 所在資料夾路徑
![](https://i.imgur.com/ujhQw5P.png)
上傳成功的話會回傳一個帶有 uuid 及 upload_time 的 list
![](https://i.imgur.com/AI6TRfW.png)

### 圖片上傳
初始化實例後，調用 `upload_imgs` 方法傳入圖片所在資料夾路徑
![](https://i.imgur.com/VNcilsx.png)
上傳成功的話會回傳一個帶有 uuid 及 upload_time 的 list
![](https://i.imgur.com/AI6TRfW.png)

### 圖片及 klf 下載
初始化實例後，調用 `download_imgs_and_klf_wrapper` 方法傳入要放置下載的圖片的路徑、`upload_imgs_and_klf` 回傳的 uuid 及 upload_time 的 list 及圖片篩選條件`is_deleted` True/False ，
![](https://i.imgur.com/4m6LxRr.png)
下載成功訊息
![](https://i.imgur.com/usXx02h.png)
失敗訊息
![](https://i.imgur.com/7KLHsyc.png)


### 圖片下載
初始化實例後，調用 `download_imgs_wrapper` 方法傳入要放置下載的圖片的路徑、`upload_imgs` 回傳的 uuid 及 upload_time 的 list 、圖片篩選條件`is_deleted` True/False，
![](https://i.imgur.com/hr4Ul5K.png)
下載成功訊息
![](https://i.imgur.com/usXx02h.png)
失敗訊息
![](https://i.imgur.com/7KLHsyc.png)
