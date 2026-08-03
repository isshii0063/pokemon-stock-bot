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
    "User-Agent": "Mozilla/5.0"
}


def check_stock(name, url):
    print(f"===== {name} =====")

    r = requests.get(url, headers=HEADERS, timeout=15)

    print(f"HTTP: {r.status_code}")

    html = r.text

    # 売り切れ判定
    soldout_words = [
        "ご注文できない商品",
        "ご購入できない商品",
        "現在ご注文いただけません",
        "売り切れました",
        "在庫切れ",
        "品切れ",
    ]

    for w in soldout_words:
        if w in html:
            print("→ 売り切れ判定")
            return False

    print("→ 在庫あり判定")
    return True


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
            print(f"✅ {name}: 通知送信")
        else:
            print(f"❌ {name}: 在庫なし")

    except Exception as e:
        print(f"🚨 エラー: {name} - {e}")