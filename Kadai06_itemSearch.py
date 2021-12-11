import os
import sys
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

SEARCH_FILE_PATH = f'./search/rakuten_{keyword}_{current_datetime}.csv'
os.makedirs(os.path.dirname(SEARCH_FILE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

REQUEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?'

#キーワードで検索した結果何件検索されるか⇒検索件数
params = {
    'keyword': keyword,
    'applicationId': APP_ID,
}

res = requests.get(REQUEST_URL, params)
result = res.json()

total = result['count']
functions.make_log(f'検索件数取得:{total}')
if total == 0:
  print('該当の商品は見つかりませんでした。\n検索を終了します。')
  
else:
  print(f'検索件数：{total}')

  #検索された全件は何ページ分になるか
  pages = int(total / 30) + 1
  print(f'ページ数：{pages}')
  functions.make_log(f'ページ総数取得:{pages}')
  
  #取得可能な最大ページ数
  MAX = 100
  if pages > MAX:
    pages = MAX
  functions.make_log(f'情報取得ページ数設定:{pages}')
  #情報取得
  row = []
  try:
    functions.make_log('情報取得開始')
    # for i in range(pages):
    for i in range(1,pages+1):
      print(f'{i}ページ目を取得')
      functions.make_log(f'{i}ページ目を取得')
      params = {
          'keyword': keyword,
          'applicationId':APP_ID,
          'page': i,
      }

      res = requests.get(REQUEST_URL, params)
      result = res.json()
      items_info = result['Items']
      for j, item_info in enumerate(items_info):
        item_name = item_info['Item']['itemName'][:30]
        item_price = item_info['Item']['itemPrice']
        item_genreId = item_info['Item']['genreId']
        item_URL = item_info['Item']['itemUrl']
        item_shopname = item_info['Item']['shopName']
        item_shopURL = item_info['Item']['shopUrl']
        row.append([item_name, item_price, item_genreId, item_URL, item_shopname, item_shopURL])
      time.sleep(0.5)
  except:
    functions.has_error()
    print('続けます。')
  print('データ取得完了')
  functions.make_log('データ取得完了')

  col = ['商品名', '価格','ジャンルId','商品URL','店名','店URL']
  df = pandas.DataFrame(row, columns=col)
  df.to_csv(SEARCH_FILE_PATH, index=False, encoding='utf_8_sig')

  print('検索結果をcsvファイルに保存しました。')
  functions.make_log('検索結果をcsvファイルに保存')
  #最高値
  high_price = df['価格'].max()
  #最安値
  low_price = df['価格'].min()

  print(f'最高値：{high_price:,}円')
  print(f'最安値：{low_price:,}円')

  # id_mode = df['GenreId'].mode()[0]
  # print(f'最も多いジャンルIDは{id_mode}です。')



