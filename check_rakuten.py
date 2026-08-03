def check_stock(name, url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    html = r.text

    print(f"{name}: HTTP {r.status_code}")

    # 売り切れ系の文字があれば在庫なし
    soldout_words = [
        "ご注文できない商品",
        "現在ご注文いただけません",
        "売り切れました",
        "在庫切れ",
        "品切れ",
    ]

    for w in soldout_words:
        if w in html:
            return False

    # それ以外で正常ページなら在庫あり扱い
    return r.status_code == 200