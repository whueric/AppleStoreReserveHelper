import webbrowser
from availability import check_availability
from threading import Timer
from datetime import datetime


# 参照README.md的零售店对照表
BUY_CITY = '上海'
BUY_STORE = 'R390'
# 参照README.md的SKU对照表
BUY_MODEL = 'MGLH3CH/A'
# 参照README.md的颜色对照表
# BUY_COLOR = '海蓝色'

RESERVE_URL = r'https://reserve-prime.apple.com/CN/zh_CN/reserve/A/availability?store={0}&iUP=N&appleCare=N&rv=0&partNumber={1}'


class AppleStoreMonitorTimer:
    def __init__(self):
        self.monitor_and_reserve()

    def monitor_and_reserve(self):
        store_num, store_name = check_availability(BUY_CITY, BUY_MODEL)
        now = datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        print('=' * 40)
        if store_name:
            print('%s %s %s 有货!!！' % (ts, store_name, BUY_MODEL))
            webbrowser.open(RESERVE_URL.format(BUY_STORE, BUY_MODEL))
            # return
        else:
            print('%s %s %s 无货！' % (ts, BUY_CITY, BUY_MODEL))
        Timer(5, self.monitor_and_reserve).start()


if __name__ == '__main__':
    AppleStoreMonitorTimer()
