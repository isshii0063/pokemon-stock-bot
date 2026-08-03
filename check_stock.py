def check_stock(name, url):
    print(f"===== {name} =====")

    r = requests.get(url, timeout=15)

    print(f"HTTP: {r.status_code}")

    html = r.text

    # イオンの在庫あり判定
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