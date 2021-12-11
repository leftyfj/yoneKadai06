import os
import sys
import requests
import pandas
import time
import datetime

current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

keyword = input('検索したい商品名: ')

SEARCH_FILE_PATH = f'./search/rakuten_{keyword}_{current_datetime}.csv'
LOG_FILE_PATH = f'./log/log_{current_date}.txt'
os.makedirs(os.path.dirname(SEARCH_FILE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

REQUEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?'
APP_ID = '1047038784147248420'



#キーワードで検索した結果何件検索されるか⇒検索件数
params = {
    'keyword': keyword,
    'applicationId': APP_ID
}

res = requests.get(REQUEST_URL, params)
result = res.json()
total = result['count']

if total == 0:
  print('該当の商品は見つかりました。')
else:
  print(f'検索件数：{total}')

  #検索された全件は何ページ分になるか
  pages = int(total / 30) + 1
  print(f'ページ数：{pages}')

  #情報取得
  row = []
  # for i in range(pages):
  for i in range(1,pages+1):
    print(f'{i}ページ目を取得')
    params = {
        'keyword': keyword,
        'applicationId':APP_ID,
        'page': i,
    }

    res = requests.get(REQUEST_URL, params)
    result = res.json()
    items_info = result['Items']

    for j, item_info in enumerate(items_info):
      item_name = item_info['Item']['itemName'][:10]
      item_price = item_info['Item']['itemPrice']
      item_genreId = item_info['Item']['genreId']
      row.append([item_name, item_price, item_genreId])
      
    time.sleep(0.5)

  print('データ取得完了')

  col = ['Name', 'Price','GenreId']
  df = pandas.DataFrame(row, columns=col)
  df.to_csv(SEARCH_FILE_PATH, index=False, encoding='utf_8_sig')

  # print(df.describe())
  #最高値
  high_price = df['Price'].max()
  #最安値
  low_price = df['Price'].min()

  print(f'最高値：{high_price:,}円')
  print(f'最安値：{low_price:,}円')

  id_mode = df['GenreId'].mode()[0]
  print(f'最も多いジャンルIDは{id_mode}です。')
  print(type(id_mode))


