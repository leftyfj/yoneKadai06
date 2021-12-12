import os
import requests
import pandas
import time
import datetime
import functions
from config import *

global keyword

current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

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
    functions.make_log('情報取得開始')
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
    functions.has_error()
   
  return rows 

def find_genreId_mode(rows):
  col = ['Item','GenreId']
  df = pandas.DataFrame(rows, columns=col)
  id_mode = df['GenreId'].mode()[0]
  print(f'検索した商品はジャンルID{id_mode}に属しています。\nジャンルID{id_mode}のランキングを取得します。')
  
  return id_mode

def make_itemRanking_by_genreId_mode(id_mode):
  params = {
      'applicationId': APP_ID,
      'genreId': id_mode,
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
  df = pandas.DataFrame(rows, columns=col)
  # GENRERANKING_FILE_PATH = f'./search/rakuten_genreranking_{keyword}_{current_datetime}.csv'
  # df.to_csv(GENRERANKING_FILE_PATH, index=False, encoding='utf_8_sig')
  return df

def save_data_in_csv_file(data, path):
  os.makedirs(os.path.dirname(path), exist_ok=True)
  data.to_csv(path, index=False, encoding='utf_8_sig')

def main():
  functions.make_log('検索開始')
  keyword = input('検索したい商品名: ')
  total = check_counts_of_items_by_keyword(keyword, APP_ID)

  if total == 0:
    functions.make_log('該当の商品なし。検索終了。')
    print('該当の商品は見つかりませんでした。\n検索を終了します。')
  else:
    pages = set_pages_by_total_items(total)
    print(f'検索された商品:{total}件')
    functions.make_log(f'検索された商品:{total}件')
    
    try:
      rows = []
      functions.make_log('ランキング情報取得開始')
      rows = search_items_detail(keyword, pages)
      genreId_mode = find_genreId_mode(rows)
      
      genreranking_file_path = f'./search/rakuten_genreranking_{keyword}_{current_datetime}.csv'
      data = make_itemRanking_by_genreId_mode(genreId_mode)
      save_data_in_csv_file(data, genreranking_file_path)
 
    except:
      functions.has_error()
    print('ランキングを作成しcsvファイルに保存しました。')
    functions.make_log('ランキング作成完了')

if __name__ == "__main__":
    main()
