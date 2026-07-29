import requests
import os

webhook = os.environ["DISCORD_WEBHOOK"]

requests.post(webhook, json={
    "content": "🎉 ポケカ監視Bot テスト成功！"
})

print("Discordへ送信しました")
