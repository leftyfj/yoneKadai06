import datetime

current_date = datetime.datetime.now().strftime('%Y-%m-%d')

APP_ID = '1047038784147248420'
LOG_FILE_PATH = f'./log/log_{current_date}.txt'

#GCP関連
SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'gcp-python-334911-46959ca421ac.json'
SPREADSHEET_KEY = '1Us3CMgJ_voLoxAx4DH0pXQxbpCDmwvUk68XX597MWRw'
