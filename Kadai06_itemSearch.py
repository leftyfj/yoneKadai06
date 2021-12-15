import os

import pandas
import time
import datetime
import functions
from config import *
from logger import set_logger
logger = set_logger(__name__)

current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

def main():
  # functions.make_log('検索開始')
  logger.info('検索開始')
  keyword = input('検索したい商品名: ')
  
  total = functions.check_counts_of_items_by_keyword(keyword, APP_ID)
  # functions.make_log(f'検索件数取得:{total}')
  # print(f'検索された商品:{total}件')
  logger.info(f'検索された商品:{total}件')
  if total == 0:
    # functions.make_log('該当の商品なし。検索終了。')
    logger.info('該当の商品なし。検索終了。')
    # print('該当の商品は見つかりませんでした。\n検索を終了します。')
    logger.info('該当の商品は見つかりませんでした。\n検索を終了します。')
  else:
    pages = functions.set_pages_by_total_items(total)
    if pages == 100:
      # print('楽天市場の規準により3000件、100ページ分の情報を取得します。')
      # functions.make_log('楽天市場の規準により3000件、100ページ分の情報を取得開始')
      logger.info('楽天市場の規準により3000件、100ページ分の情報を取得開始')
    else:
      # print(f'{total}件、{pages}ページ分の情報を取得します。')
      # functions.make_log('{total}件、{pages}ページ分の情報開始')
      logger.info(f'{total}件、{pages}ページ分の情報開始')
    rows = functions.search_items_detail(keyword, pages, show_progress=True)
    # print('データ取得完了')
    # functions.make_log('データ取得完了')
    logger.info('データ取得完了')
    col = ['商品名', '価格', 'ジャンルId', '商品URL', '店名', '店URL']
    df = pandas.DataFrame(rows, columns=col)
    df = df.sort_values('価格')
    
    search_file_path = f'./search/rakuten_{keyword}_{current_datetime}.csv'
    os.makedirs(os.path.dirname(search_file_path), exist_ok=True)
    functions.save_data_in_csv_file(df, search_file_path)
    
    # print('検索結果を価格の安い順にcsvファイルに保存しました。')
    # functions.make_log('検索結果をcsvファイルに保存(価格を昇順にソート)')
    logger.info('検索結果をcsvファイルに保存(価格を昇順にソート)')
    #最高値
    high_price = df['価格'].max()
    #最安値
    low_price = df['価格'].min()
    print('検索された商品の')
    print(f'最高値：{high_price:,}円')
    print(f'最安値：{low_price:,}円')
    
    
if __name__ == "__main__":
    main()


