import os
import requests

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

PRODUCTS = {
    "インフェルノX": "https://aeonretail.com/product/0/P-4902370552769/",
    "メガドリームEX": "https://aeonretail.com/product/0/P-4902370552745/",
    "スタートデッキGenerations": "https://aeonretail.com/product/0/P-4521329364668/",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def check_stock(name, url):
    print(f"===== {name} =====")

    r = requests.get(url, headers=HEADERS, timeout=15)

    print(f"HTTP: {r.status_code}")

    html = r.text

    stock_words = [
        "カートに入れる",
        "購入する",
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
                f"🎉 イオン在庫あり！\\n"
                f"📦 {name}\\n"
                f"🔗 {url}"
            )
            send_discord(msg)
            print(f"✅ {name}: 通知送信")
        else:
            print(f"❌ {name}: 在庫なし")

    except Exception as e:
        print(f"🚨 エラー: {name} - {e}")