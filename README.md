# Hoyo Helper

This is a hoyo helper intended to help user check-ins automatically, and sending notification to discord webhook

## Setting Up

### Credentials

Obtain the required 3 credentials:
1. HOYO_TOKENS
2. DISCORD_WEBHOOK

You require the cookies containing `ltuid` and `ltoken` to be able to construct `HOYO_TOKENS`.

The format of the credentials can be seen as the following [helper.py](./helper.py):

```python
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
```

*games* field must be one of `(gs, hsr, hi3)`

Supports multiple tokens, in case you want to do it for multiple accounts


### Mihoyo Authentication Update

Mihoyo might have updated their authentication to use `ltuid_v2` and `ltoken_v2` instead. You can modify `HOYO_TOKENS` to change/add `enable_v2` as shown below, and use it when generating the required secrets to be passed in github's action secret

```python
HOYO_TOKENS = [
    {
        "ltoken": "xxx",
        "ltuid": 123,
        "games": ["gs", "hsr"],
        "enable_v2": True,
    },
]
```

### Discord UID?

Pass in `discord_uid` for `HOYO_TOKENS` to enhance the discord notification if you want to.

```python
HOYO_TOKENS = [
    {
        "ltoken": "xxx",
        "ltuid": 123,
        "games": ["gs", "hsr"],
        "discord_uid": 123,
    },
]
```

## Local Development / Testing

### Installing
```bash
git clone https://github.com/T-kON99/Hoyo-Helper.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Duplicate [helper.py](./helper.py) to `secret.py` and fill in with correct information. 

You can now run `./run.sh` directly.

## Footnotes

1. Utilizes github workflows to run the job once per day
2. When passing in secrets to github workflow, make sure the json format of the token is minified and a valid json (use [helper.py](./helper.py) for easier setup)
3. Related `ltoken/ltuid` cookie has expiration date, but usually it's very long in the future. Thus the cookie may or may not be valid after that time, and will require to be renewed
4. You have to re-enable workflow periodically every 60 days.
