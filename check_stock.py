import os
from playwright.sync_api import sync_playwright

DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

PRODUCTS = {
    "インフェルノX": "https://aeonretail.com/product/0/P-4902370552769/",
    "メガドリームEX": "https://aeonretail.com/product/0/P-4902370552745/",
    "スタートデッキGenerations": "https://aeonretail.com/product/0/P-4521329364668/",
}


def check_stock(name, url):
    print(f"===== {name} =====")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/120.0 Safari/537.36"
            )
        )

        try:
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            html = page.content()

            stock_words = [
                "カートに入れる",
                "購入する",
                "予約する",
                "在庫あり",
            ]

            for word in stock_words:
                if word in html:
                    print(f"→ 在庫あり ({word})")
                    browser.close()
                    return True

            print("→ 在庫なし")
            browser.close()
            return False

        except Exception as e:
            print(f"🚨 エラー: {e}")
            browser.close()
            return False


def send_discord(message):
    import requests

    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message},
        timeout=10
    )


for name, url in PRODUCTS.items():

    try:
        if check_stock(name, url):

            msg = (
                "🎉 イオンポケカ在庫あり！\n"
                f"📦 {name}\n"
                f"🔗 {url}"
            )

            send_discord(msg)

            print(f"✅ {name}: 通知送信")

        else:
            print(f"❌ {name}: 在庫なし")

    except Exception as e:
        print(f"🚨 エラー: {name} - {e}")