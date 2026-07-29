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

for name, url in PRODUCTS.items():
    try:
        r = requests.get(url, headers=headers, timeout=15)
        text = r.text

        if "カートに入れる" in text or "購入する" in text:
            requests.post(webhook, json={
                "content": f"🔔 【イオン在庫あり】\n{name}\n{url}"
            })
            print(f"{name}: 在庫あり")
        else:
            print(f"{name}: 在庫なし")

    except Exception as e:
        print(f"{name}: エラー {e}")
