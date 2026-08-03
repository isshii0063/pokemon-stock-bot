def check_stock(name, url):
    print(f"===== {name} =====")

    r = requests.get(url, headers=HEADERS, timeout=15)

    print(f"HTTP: {r.status_code}")

    html = r.text

    # 楽天ブックス購入可能ワード
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