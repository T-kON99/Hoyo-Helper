import json
import sys
import logging

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/xxx/xxx"
HOYO_TOKENS = [
    {
        "ltoken": "xxx",
        "ltuid": 123,
        "games": ["gs", "hsr"],
    },
]


def minify(d) -> str:
    return json.dumps(d)


if __name__ == "__main__":
    tokenStr = minify(HOYO_TOKENS)
    logging.basicConfig(encoding="utf-8", level=logging.INFO, stream=sys.stdout)
    logging.info(f"HOYO_TOKENS: {tokenStr}")
    logging.info(f"DISCORD_WEBHOOK: {DISCORD_WEBHOOK}")
