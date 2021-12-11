import os
import requests
import pandas
import time
import datetime
import functions
from config import *

current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

functions.make_log('検索開始')
keyword = input('検索したい商品名: ')

GENRERANKING_FILE_PATH = f'./search/rakuten_genreranking_{keyword}_{current_datetime}.csv'
os.makedirs(os.path.dirname(GENRERANKING_FILE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

REQUEST_ITEM_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?'
REQUEST_RANKING_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?'

params = {
    'keyword': keyword,
    'applicationId': APP_ID,
}

res = requests.get(REQUEST_ITEM_URL, params=params)
result = res.json()
total = result['count']
if total == 0:
  print('該当の商品は見つかりませんでした。\n検索を終了します。')
else:
  # 検索された全件は何ページ分になるか
  pages = int(total / 30) + 1
  #取得可能な最大ページ数
  MAX = 100
  if pages > MAX:
    pages = MAX

  row = []
  try:
    functions.make_log('情報取得開始')
    for i in range(1, pages+1):
      params = {
          'keyword': keyword,
          'applicationId': APP_ID,
          'page': i,
      }

      res = requests.get(REQUEST_ITEM_URL, params=params)
      result = res.json()
      items_info = result['Items']
      for j, item_info in enumerate(items_info):
        item_name = item_info['Item']['itemName'][:30]
        item_genreId = item_info['Item']['genreId']
        row.append([item_name,item_genreId])
      time.sleep(0.5)
  except:
    functions.has_error()
    
  col = ['Item','GenreId']
  df = pandas.DataFrame(row, columns=col)
  
  genreId_mode = df['GenreId'].mode()[0]
  print(f'検索した商品はジャンルID{genreId_mode}に属しています。\nジャンルID{genreId_mode}のランキングを取得します。')
  
  params = {
      'applicationId': APP_ID,
      'genreId': genreId_mode,
  }

  res = requests.get(REQUEST_RANKING_URL,params=params)
  result = res.json()
  items_info = result['Items']

  rows = []
  for item_info in items_info:
    item_rank = item_info['Item']['rank']
    item_name = item_info['Item']['itemName'][:30]
    item_price = item_info['Item']['itemPrice']
    item_URL = item_info['Item']['itemUrl']
    item_shopname = item_info['Item']['shopName']
    item_shopURL = item_info['Item']['shopUrl']
    item_genreId = item_info['Item']['genreId']
    rows.append([item_rank, item_name, item_price, item_URL,
                item_shopname, item_shopURL, item_genreId])
  time.sleep(0.5)

  col = ['順位', '商品名','価格','商品URL','店名','店URL','ジャンルID']
  df2 = pandas.DataFrame(rows, columns=col)
  df2.to_csv(GENRERANKING_FILE_PATH, index=False, encoding='utf_8_sig')
