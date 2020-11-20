import json
import requests
from retrying import retry


@retry(stop_max_attempt_number=5)
def get_stores():
    url = r'https://reserve-prime.apple.com/CN/zh_CN/reserve/A/stores.json'
    headers = {'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en-US;q-0.8,en;q-0.7',
               'referer': 'https://reserve-prime.apple.com/CN/zh_CN/reserve/A/availability?&iUP=N',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/87.0.4280.67 Safari/537.36',
               }

    cookie_str = r'dslang=CN-ZH; site=CHN; geo=CN; ccl=WwsyNcK54j2kPzLwbGGJHw==; s_orientation=%5B%5BB%5D%5D; ' \
                 r's_cc=true; check=true; s_campaign=mc-ols-energy_saver-article_ht211094-macos_ui-04022020; dssf=1; ' \
                 r'XID=1e2b043fd33526cd0d7f7b5962bb4cc1; POD=cn~zh; JSESSIONID=8B7AC75267A9983B21AAB8AD19CD5965; '
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie_str.split("; ")}

    resp = requests.get(url, cookies=cookie_dict, headers=headers).content
    result = json.loads(resp)
    return result


def get_store_number(city=None):
    res = get_stores()
    stores = res['stores']
    buy_stores = []
    if city is None:
        for store in stores:
            buy_stores.append((store['storeNumber'], store['city'] + store['storeName']))
    else:
        for store in stores:
            if store['city'] == city:
                buy_stores.append((store['storeNumber'], store['city'] + store['storeName']))

    return buy_stores
