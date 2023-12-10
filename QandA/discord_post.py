# Reference

import json
from urllib.request import Request, urlopen
import environ

env = environ.Env()
env.read_env('.env')

WEBHOOK_URL = env('DISCORD_WEBHOOK')

def post_discord(message: str):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (private use) Python-urllib/3.10",
    }
    data = {"content": message}
    request = Request(
        WEBHOOK_URL,
        data=json.dumps(data).encode(),
        headers=headers,
    )

    with urlopen(request) as res:
        assert res.getcode() == 204

