# coding:utf-8
import time
import os
from datetime import datetime
from selenium import webdriver

LOGIN_ID = 'kitatakisan@gmail.com'
LOGIN_PASSWORD = 'kenta3054'

ITEM_URL = 'https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-%E3%83%AA%E3%83%B3%E3%82%B0%E3%83%95%E3%82%A3%E3%83%83%E3%83%88-%E3%82%A2%E3%83%89%E3%83%99%E3%83%B3%E3%83%81%E3%83%A3%E3%83%BC-Switch/dp/B07XV8VSZT/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3UB7LC2MWWEYP&dchild=1&keywords=%E3%83%AA%E3%83%B3%E3%82%B0%E3%83%95%E3%82%A3%E3%83%83%E3%83%88%E3%82%A2%E3%83%89%E3%83%99%E3%83%B3%E3%83%81%E3%83%A3%E3%83%BC&qid=1597763365&sprefix=%E3%83%AA%E3%83%B3%E3%82%B0%E3%83%95%E3%82%A3%E3%83%83%E3%83%88%2Caps%2C273&sr=8-1'

ACCEPT_SHOP = 'Amazon'
LIMIT_VALUE = 9000

def check():
    b.get(ITEM_URL)
    while True:
        dt_time = datetime.now()
        if 9 <= dt_time.hour <= 11:
            try:
                #販売元確認
                shop = b.find_element_by_id('merchant-info').text
                shop = shop.split('が販売')[0].split('この商品は、')[1]
                p = b.find_element_by_css_selector('.a-span12 .priceBlockBuyingPriceString').text
                p = int(p.split('￥')[1].replace(',',''))

                s = shop + ':' + str(p)
                print(s)

                if p > LIMIT_VALUE:
                    raise Exception("not Price.")

                if ACCEPT_SHOP not in shop:
                    raise Exception("not Amazon.")


                #カートに入れる

                b.find_element_by_id('add-to-cart-button').click()
                break

            except:
                time.sleep(20)
                b.refresh()
    cart()

def cart():
    while True:
    #カレントページのURLを取得
        cur_url = b.current_url
        #カート画面に飛ばなければ更新
        if 'https://www.amazon.co.jp/gp/product/handle-buy-box/ref=dp_start-bbf_1_glance' in cur_url:
            try:
                time.sleep(5)
                b.find_element_by_css_selector('.a-button-text.a-text-center').click()
                print("True")
                break
            except:
                time.sleep(60)
                print('not cart')
                check()
        else:
            print(cur_url)
            time.sleep(20)
            b.refresh()
    '''
    #購入手続き
    b.get('https://www.amazon.co.jp/gp/cart/view.html?ref_=nav_cart')
    b.find_element_by_name('proceedToRetailCheckout').click()
    #購入画面に飛ばなければ更新
    while True:
        #カレントページのURLを取得
        cur_url = b.current_url
        if 'https://www.amazon.co.jp/ap/signin?_encoding=UTF8' in cur_url:
            break
        else:
            time.sleep(60)
            b.refresh()
    '''
    #ログイン
    cur_url = b.current_url
    if 'https://www.amazon.co.jp/ap/signin' in cur_url:
        try :
            time.sleep(2)
            b.find_element_by_id('ap_email').send_keys(LOGIN_ID)
            b.find_element_by_id('continue').click()
            time.sleep(1)
            b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
            b.find_element_by_id('signInSubmit').click()
        except:
            print('LOGIN PASS.')
            pass
    #注文画面飛ばなければ更新
    while True:
        #カレントページのURLを取得
        cur_url = b.current_url
        if 'https://www.amazon.co.jp/gp/buy/spc/handlers/display.html?' in cur_url:
            break
        elif 'https://www.amazon.co.jp/gp/yourstore?ie=UTF8&ref=ox_checkout_redirects_yourstore' in cur_url:
            check()
        elif 'https://www.amazon.co.jp/gp/buy/addressselect/handlers/display.html?hasWorkingJavascript=1' in cur_url:
            b.find_element_by_css_selector('.a-declarative.a-button-text').click()
            break
        else:
            print('not order')
            time.sleep(60)
            b.refresh()

    #注文の確定

    b.find_element_by_name('placeYourOrder1').click()
    #購入されなければ更新
    while True:
        #カレントページのURLを取得
        cur_url = b.current_url
        if 'https://www.amazon.co.jp/gp/buy/thankyou/handlers/display.html?ie=UTF8' in cur_url:
            break
        else:
            print('not buy')
            time.sleep(60)
            b.refresh()

    print('Finish!')
    exit()

def l(str):
    print("%s : %s"%(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),str))

if __name__ == '__main__':

    #ブラウザ起動
    try:
        userdata_dir = 'UserData'  # カレントディレクトリの直下に作る場合
        os.makedirs(userdata_dir, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument('--user-data-dir=' + userdata_dir)

        b = webdriver.Chrome(options=options)
        check()
    except:
        l('Failed to open browser')
        exit()
