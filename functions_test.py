from config import *
from functions import *
import pandas

keyword = 'ゴルフボール'
def test_check_counts_of_items_by_keyword():
  res = check_counts_of_items_by_keyword(keyword, APP_ID)
  assert res >= 0

total = 11
def test_set_pages_by_total_items():
  res = set_pages_by_total_items(total)
  assert res >= 0

def test_search_items_detail():
  rows = search_items_detail(keyword, 2)
  assert len(rows) >= 0


def test_save_data_in_csv_file():
  list = ["a1", "a2", "a3"]
  df = pandas.DataFrame(data=list)
  search_file_path = f'./search/rakuten_test.csv'
  save_data_in_csv_file(df, search_file_path)
