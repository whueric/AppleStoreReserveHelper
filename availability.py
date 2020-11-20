import json
import requests
from retrying import retry
from stores import get_store_number

'''
 F: 12, A: Pro, H: Mini, G: Pro Max 
'''


@retry(stop_max_attempt_number=5)
def get_availability():
    # iPhone 12
    url_iphone_12 = r'https://reserve-prime.apple.com/CN/zh_CN/reserve/F/availability.json'
    # iPhone 12 Pro
    url_iphone_12_pro = r'https://reserve-prime.apple.com/CN/zh_CN/reserve/A/availability.json'
    # iPhone 12 Mini
    url_iphone_12_mini = r'https://reserve-prime.apple.com/CN/zh_CN/reserve/H/availability.json'
    # iPhone 12 Pro Max
    url_iphone_12_pro_max = r'https://reserve-prime.apple.com/CN/zh_CN/reserve/G/availability.json'

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

    resp = requests.get(url_iphone_12_pro, cookies=cookie_dict, headers=headers).content
    result = json.loads(resp)
    return result


def check_availability(city, model):
    target_stores = get_store_number(city)
    all_availability = get_availability()
    res_store_num = None
    res_store_name = None
    for store_num, store_name in target_stores:
        try:
            model_availability = all_availability['stores'][store_num][model]['availability']
            if model_availability['contract'] or model_availability['unlocked']:
                res_store_num = store_num
                res_store_name = store_name
                break
        except KeyError:
            pass
    return res_store_num, res_store_name


def show_availability(model=None):
    all_stores = get_store_number()
    all_availability = get_availability()
    in_stock = []
    result = {}
    for store_num, store_name in all_stores:
        try:
            model_availability = all_availability['stores'][store_num][model]['availability']
            result[store_name] = model_availability
            if model_availability['contract'] or model_availability['unlocked']:
                in_stock.append(store_name)
        except KeyError:
            pass
    return result, in_stock
