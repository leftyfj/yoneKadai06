# https://hituji-ws.com/code/python/python-spreadsheet/
# 【python できること】 Googleスプレッドシートにデータを読み書きする方法
import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials
from config import *
from logger import set_logger
logger = set_logger(__name__)
# TODO:
def save_data_in_google_spreadsheet(dataframe,worksheetname):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, SCOPES)
    gs = gspread.authorize(credentials)
    workbook = gs.open_by_key(SPREADSHEET_KEY)
    worksheet = workbook.worksheet(worksheetname)
    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist()