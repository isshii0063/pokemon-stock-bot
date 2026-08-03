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

    # 購入可能ワード
    stock_words = [
        "買い物かごに入れる",
        "予約する",
        "購入手続きへ",
    ]

    for w in stock_words:
        if w in html:
            print(f"→ 在庫あり判定 ({w})")
            return True

    print("→ 在庫なし判定")
    return False


def send_discord(message):
    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message},
        timeout=10,
    )


# ===== 実行部分 =====
for name, url in PRODUCTS.items():
    try:
        if check_stock(name, url):
            msg = (
                f"🎉 楽天ブックス在庫あり！\\n"
                f"📦 {name}\\n"
                f"🔗 {url}"
            )
            send_discord(msg)
            print(f"✅ {name}: 通知送信")
        else:
            print(f"❌ {name}: 在庫なし")

    except Exception as e:
        print(f"🚨 エラー: {name} - {e}")