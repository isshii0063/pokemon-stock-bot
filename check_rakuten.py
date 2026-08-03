def check_stock(name, url):
    r = requests.get(url, headers=HEADERS, timeout=15)

    print(f"{name}: HTTP {r.status_code}")

    html = r.text

    # デバッグ用（最初だけ確認）
    print(html[:2000])

    # 在庫なし判定
    out_keywords = [
        "ご注文できない商品",
        "ご購入できない商品",
        "現在ご注文いただけません",
        "売り切れました",
        "在庫切れ",
        "品切れ",
    ]

    for keyword in out_keywords:
        if keyword in html:
            return False

    # 在庫あり判定
    in_keywords = [
        "買い物かご",
        "かごに追加",
        "ご注文手続きへ",
        "予約受付中",
        "予約する",
    ]

    for keyword in in_keywords:
        if keyword in html:
            return True

    return False