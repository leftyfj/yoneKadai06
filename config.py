import datetime

current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

SEARCH_FILE_PATH = f'./search/rakuten_{keyword}_{current_datetime}.csv'
LOG_FILE_PATH = f'./log/log_{current_date}.txt'

