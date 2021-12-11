import datetime
import traceback

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
