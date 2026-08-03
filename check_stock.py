from playwright.sync_api import sync_playwright
import os
import requests

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

PRODUCTS = {
    "インフェルノX": "https://aeonretail.com/product/0/P-4902370552769/",
    "メガドリームEX": "https://aeonretail.com/product/0/P-4902370552745/",
    "スタートデッキGenerations": "https://aeonretail.com/product/0/P-4521329364668/",
}


def send_discord(message):
    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message},
        timeout=10,
    )


def check_stock(name, url):
    print(f"===== {name} =====")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        # ← ここを domcontentloaded にしてタイムアウトを防ぐ
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000,
        )

        html = page.content()

        browser.close()

    if "カートに入れる" in html or "購入する" in html:
        print("→ 在庫あり")
        return True

    print("→ 在庫なし")
    return False


for name, url in PRODUCTS.items():
    try:
        if check_stock(name, url):
            send_discord(
                f"🎉 イオン在庫あり！\\n"
                f"📦 {name}\\n"
                f"🔗 {url}"
            )
            print(f"✅ {name}: 通知送信")
        else:
            print(f"❌ {name}: 在庫なし")

    except Exception as e:
        print(f"🚨 エラー: {name} - {e}")