import requests
import json


URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
TIMEOUT = 10
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"}


#サイトにアクセスする
try:
    result = requests.get(URL, timeout=TIMEOUT, headers=HEADERS)
    result.raise_for_status()
except Exception as e:
    print("ERROR_DOWNLOAD:{}".format(e))
else:
    #print(result.content)

    content = result.content

    #print(type(content))

    #jsonのbyteデータを辞書型に変換
    data    = json.loads(content)

    #天気を取得(日付、地域名、天気の順)
    print(data[0]["timeSeries"][0]["timeDefines"])
    print(data[0]["timeSeries"][0]["areas"][0]["area"])
    print(data[0]["timeSeries"][0]["areas"][0]["weathers"])
    print(data[0]["timeSeries"][0]["areas"][0]["winds"])
    print(data[0]["timeSeries"][0]["areas"][0]["waves"])

    #スペースがユニコードだがひとつづつ取り出せば大丈夫。
    for w in data[0]["timeSeries"][0]["areas"][0]["weathers"]:
        print(w.replace("　"," "))


    #気温を取得する(実行する時間帯によっては今日の気温を取得できない？ 21時44分実行で確認)
    print(data[1]["timeSeries"][1]["timeDefines"])
    print(data[1]["timeSeries"][1]["areas"][0]["area"])
    print(data[1]["timeSeries"][1]["areas"][0]["tempsMin"])
    print(data[1]["timeSeries"][1]["areas"][0]["tempsMinUpper"])
    print(data[1]["timeSeries"][1]["areas"][0]["tempsMinLower"])
    print(data[1]["timeSeries"][1]["areas"][0]["tempsMax"])
    print(data[1]["timeSeries"][1]["areas"][0]["tempsMaxUpper"])
    print(data[1]["timeSeries"][1]["areas"][0]["tempsMaxLower"])



    #=====上記データを整形して、管理サイトにアクセス、管理サイトのフォームにて新規作成する。============
    #詳細:https://noauto-nolife.com/post/python-requests-post-method/
    

    import requests,bs4
    
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

    post_data   = {
            "csrfmiddlewaretoken":csrftoken,
            "place":"広島",
            "dt_0":"2022-01-05",
            "dt_1":"10:00:00",
            "today":"晴れ",
            "tomorrow":"くもり",
            "today_high_temp":"12",
            "today_low_temp":"4",
            "tomorrow_high_temp":"8",
            "tomorrow_low_temp":"0",
            }

    r   = client.post(POST_URL,data=post_data,headers=HEADERS)
    print(r)

