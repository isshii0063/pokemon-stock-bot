import requests
import os

PRODUCTS = {
    "インフェルノX": "https://aeonretail.com/product/0/P-2135500001757/",
    "メガドリーム": "https://aeonretail.com/product/0/P-2135500002662/",
    "スタートデッキ100": "https://aeonretail.com/product/0/P-4521329427270/"
}

webhook = os.environ["DISCORD_WEBHOOK"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

results = []

for name, url in PRODUCTS.items():
    try:
        r = requests.get(url, headers=headers, timeout=15)
        text = r.text

        if "カートに入れる" in text or "購入する" in text:
            results.append(f"🟢 {name}: 在庫あり！ {url}")

    except Exception as e:
        print(f"{name}: エラー {e}")

# 在庫ありの商品がある時だけ通知
if results:
    requests.post(webhook, json={
        "content": "🚨 イオン在庫復活！\\n\\n" + "\\n".join(results)
    })
