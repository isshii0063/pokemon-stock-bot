import os
import requests

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

PRODUCTS = {
    "ストームエメラルダ": "https://books.rakuten.co.jp/rb/18537078/",
    "インフェルノX": "https://books.rakuten.co.jp/rb/18287437/",
    "メガドリームEX": "https://books.rakuten.co.jp/rb/18343992/",
    "スタートデッキGenerations": "https://books.rakuten.co.jp/rb/18548589/",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )
}


def check_stock(name, url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    html = r.text

    # 在庫なし判定
    out_keywords = [
        "ご購入できない商品",
        "在庫切れ",
        "売り切れ",
        "現在ご購入いただけません",
    ]

    for keyword in out_keywords:
        if keyword in html:
            return False

    # 在庫あり判定
    in_keywords = [
        "買い物かごに入れる",
        "ご購入手続きへ",
        "予約受付中",
    ]

    for keyword in in_keywords:
        if keyword in html:
            return True

    # 判定できない場合はログ確認用
    print(f"⚠️ 判定不能: {name}")
    return False


def send_discord(message):
    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message},
        timeout=10,
    )


for name, url in PRODUCTS.items():
    try:
        if check_stock(name, url):
            msg = f"🎉 楽天ブックス在庫あり！\\n📦 {name}\\n🔗 {url}"
            send_discord(msg)
            print(f"✅ {name}: 在庫あり")
        else:
            print(f"❌ {name}: 在庫なし")

    except Exception as e:
        print(f"🚨 エラー: {name} - {e}")