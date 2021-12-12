import os
import datetime
import time
import traceback
import requests

from config import *

### ログ出力関数

def make_log(txt):
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s:%s] %s' % ('log', now, txt)
    #ファイルに出力
    with open(LOG_FILE_PATH, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')

def has_error():
  make_log('例外発生')
  make_log(traceback.format_exc())
  
def check_counts_of_items_by_keyword(keyword, APP_ID):
  REQUEST_ITEM_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?'
  params = {
      'keyword': keyword,
      'applicationId': APP_ID,
  }
  res = requests.get(REQUEST_ITEM_URL, params=params)
  result = res.json()
  total = result['count']
  return total

def set_pages_by_total_items(total):
  # 検索された全件は何ページ分になるか
  pages = int(total / 30) + 1
  #取得可能な最大ページ数
  MAX = 100
  if pages > MAX:
    pages = MAX
  return pages


def search_items_detail(keyword, pages):
  # REQUEST_RANKING_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?'
  REQUEST_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?'
  rows = []
  try:
    make_log('情報取得開始')
    for i in range(1, pages+1):
      params = {
          'keyword': keyword,
          'applicationId': APP_ID,
          'page': i,
      }

      res = requests.get(REQUEST_URL, params=params)
      result = res.json()
      items_info = result['Items']
      for item_info in items_info:
        item_name = item_info['Item']['itemName'][:30]
        item_price = item_info['Item']['itemPrice']
        item_genreId = item_info['Item']['genreId']
        item_URL = item_info['Item']['itemUrl']
        item_shopname = item_info['Item']['shopName']
        item_shopURL = item_info['Item']['shopUrl']
        rows.append([item_name, item_price, item_genreId,
                     item_URL, item_shopname, item_shopURL])
      time.sleep(0.5)
  except:
    has_error()

  return rows

def save_data_in_csv_file(data, path):
  os.makedirs(os.path.dirname(path), exist_ok=True)
  data.to_csv(path, index=False, encoding='utf_8_sig')
