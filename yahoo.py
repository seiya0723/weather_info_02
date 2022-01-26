import requests,bs4,datetime

#気温に不要な文字列があるので、除去するため、正規表現のモジュールをimport(℃などの単位をそのまま管理サイトに入れると、バリデーションNGになる。)
#↑emを取得すれば正規表現も不要

#ここに取得したい地域のURLを指定。(東京であれば /13/4410.html、広島であれば /34/6710.html)

LOCALE  = [
        {"area":"東京","url":"/13/4410.html"},
        {"area":"広島","url":"/34/6710.html"},
        ]

#URL = "https://weather.yahoo.co.jp/weather/jp/34/6710.html"
URL = "https://weather.yahoo.co.jp/weather/jp" + LOCALE[0]["url"]
TIMEOUT = 10
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"}


#サイトにアクセスする
try:
    result = requests.get(URL, timeout=TIMEOUT, headers=HEADERS)
    result.raise_for_status()
except Exception as e:
    print("ERROR_DOWNLOAD:{}".format(e))
else:
    soup    = bs4.BeautifulSoup(result.content,"html.parser")
    data    = soup.select(".forecastCity")
    print(data)

    print("==========================================")

    #今日の天気の取得
    today_weather_elem  = soup.select("div.forecastCity > table > tr > td:nth-child(1) > div > p.pict")

    for t in today_weather_elem:
        print(t.text.strip())
        today   = t.text.strip()

    #今日の最高気温の取得
    today_temp_high_elem    = soup.select("div.forecastCity > table > tr > td:nth-child(1) > div > ul.temp > li.high > em")

    for t in today_temp_high_elem:
        print(t.text.strip())
        today_high_temp = t.text.strip()


    #今日の最低気温の取得
    today_temp_low_elem     = soup.select("div.forecastCity > table > tr > td:nth-child(1) > div > ul.temp > li.low > em")

    for t in today_temp_low_elem:
        print(t.text.strip())
        today_low_temp = t.text.strip()

    #明日の天気の取得
    tomorrow_weather_elem   = soup.select("div.forecastCity > table > tr > td:nth-child(2) > div > p.pict")

    for t in tomorrow_weather_elem:
        print(t.text.strip())
        tomorrow   = t.text.strip()

    #明日の最高気温の取得
    tomorrow_temp_high_elem = soup.select("div.forecastCity > table > tr > td:nth-child(2) > div > ul.temp > li.high > em")

    for t in tomorrow_temp_high_elem:
        print(t.text.strip())
        tomorrow_high_temp  = t.text.strip()

    #明日の最低気温の取得
    tomorrow_temp_low_elem  = soup.select("div.forecastCity > table > tr > td:nth-child(2) > div > ul.temp > li.low > em")

    for t in tomorrow_temp_low_elem:
        print(t.text.strip())
        tomorrow_low_temp   = t.text.strip()


    message = LOCALE[0]["area"] + "の今日と明日の天気\n\n"
    message += "今日\n"
    message += today + "\n"
    message += "最高気温:" + today_high_temp + "\n"
    message += "最低気温:" + today_low_temp + "\n\n"
    message += "明日\n"
    message += tomorrow + "\n"
    message += "最高気温:" + tomorrow_high_temp + "\n"
    message += "最低気温:" + tomorrow_low_temp + "\n\n"
    print(message)

    #=============スクレイピング部ここまで=================================================================

    print("スクレイピング完了")

    #=====上記データを整形して、管理サイトにアクセス、管理サイトのフォームにて新規作成する。============
    #詳細:https://noauto-nolife.com/post/python-requests-post-method/
    
    
    #ここにIDとパスワードを入力する。
    ID      = "asahina"
    PASS    = "seiya0723"
    
    #ここにで管理サイトのURLを入力(デプロイした後は下記URLを変更する。)
    URL     = "http://127.0.0.1:8000/"
    LOGIN   = URL + "admin/login/"
    TIMEOUT = 10
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}
    
    #(1) セッションを維持する(セッションメソッドからオブジェクトを作る)
    client = requests.session()
    r = client.get(LOGIN,timeout=TIMEOUT,headers=HEADERS)
    print(r)
    
    #(2) CSRFトークンを手に入れ、投稿するデータを辞書型で生成
    if 'csrftoken' in client.cookies:
        csrftoken = client.cookies['csrftoken']
        print(csrftoken)
    
    login_data   = { "csrfmiddlewaretoken":csrftoken,
                     "username":ID,
                     "password":PASS
                     }
    
    #(3) ログインする
    r   = client.post(LOGIN,data=login_data,headers={"Referer":LOGIN})

    #(4) ログインに使用したセッションで天気のフォームにアクセス。name属性はモデルのフィールド名と同じ。日時型は分離している点に注意
    POST_URL    = URL + "admin/tenki/weather/add/"

    #ログインした後、新規作成フォームのページにアクセスする。(CSRFトークンを手に入れるため。) 
    r = client.get(POST_URL,headers=HEADERS)
    
    #CSRFトークンをセットし直す。
    if 'csrftoken' in client.cookies:
        csrftoken = client.cookies['csrftoken']
        print(csrftoken)

    #取得日をセット
    dt      = datetime.datetime.now()
    dt_0    = dt.strftime("%Y-%m-%d")
    dt_1    = dt.strftime("%H:%M:%S")

    post_data   = {
            "csrfmiddlewaretoken":csrftoken,
            "place":"東京",
            "dt_0":dt_0,
            "dt_1":dt_1,
            "today":today,
            "tomorrow":tomorrow,
            "today_high_temp":today_high_temp,
            "today_low_temp":today_low_temp,
            "tomorrow_high_temp":tomorrow_high_temp,
            "tomorrow_low_temp":tomorrow_low_temp,
            }

    print(post_data)

    r   = client.post(POST_URL,data=post_data,headers=HEADERS)
    print(r)



    #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

    #メール送信処理。SendgridにてAPIを取得する
    import sendgrid
    from sendgrid.helpers.mail import *
    
    SENDGRID_API    = "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"
    
    sg          = sendgrid.SendGridAPIClient(api_key=SENDGRID_API)
    from_email  = Email("seiya.asahina0723@gmail.com")
    to_email    = To("seiya.asahina0723@gmail.com")
    subject     = "今日と明日の天気取得しました"
    content     = Content("text/plain", message)
    mail        = Mail(from_email, to_email, subject, content)
    response    = sg.client.mail.send.post(request_body=mail.get())

    print(response)



