import os
import requests
import pandas
import time
import datetime
import functions
from config import *
import googlespreadsheet as gss
from logger import set_logger
logger = set_logger(__name__)

global keyword

current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def make_itemRanking_by_genreId_mode(id_mode):
  REQUEST_RANKING_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?'
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

  return df

def main():
  logger.info('検索開始')
  
  keyword = input('検索したい商品名: ')
  total = functions.check_counts_of_items_by_keyword(keyword, APP_ID)

  if total == 0:
    logger.warning('該当の商品なし。検索終了。')
    print('該当の商品は見つかりませんでした。\n検索を終了します。')
  else:
    pages = functions.set_pages_by_total_items(total)
    print(f'検索された商品:{total}件')
    logger.info(f'検索された商品:{total}件')
    try:
      logger.info('ランキング情報取得開始')
      rows = functions.search_items_detail(keyword, pages)
      genreId_mode = functions.find_genreId_mode(rows)
      
      genre_name = functions.find_genre_name_by_genre_id(genreId_mode)
      genreranking_file_path = f'./search/rakuten_genreranking_{keyword} 所属ジャンル_{genreId_mode}_{current_datetime}.csv'
      data = make_itemRanking_by_genreId_mode(genreId_mode)
      gss.save_data_in_google_spreadsheet(data,'検索結果')
      # functions.save_data_in_csv_file(data, genreranking_file_path)
 
    except:
      functions.has_error()
    logger.info('ランキング作成完了。csvファイルに保存')

if __name__ == "__main__":
    main()
