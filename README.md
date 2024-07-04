# Hoyo Helper

This is a hoyo helper intended to help user check-ins automatically, and sending notification to discord webhook

## Setting Up

### Credentials

Set up these 2 [Github Action Secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository)
1. HOYO_TOKENS
2. DISCORD_WEBHOOK

You require the cookies containing `ltuid` and `ltoken` to be able to construct `HOYO_TOKENS`.

#### How to obtain HoYoLab Cookie

1. To begin, login with your [HoYoLab](https://www.hoyolab.com/home) Account or from [Battlepass](https://act.hoyolab.com/app/community-game-records-sea/index.html?bbs_presentation_style=fullscreen&bbs_auth_required=true&gid=2&user_id=122516750&utm_source=hoyolab&utm_medium=gamecard&bbs_theme=light&bbs_theme_device=1#/ys).
2. Type `java` in the address bar followed by the script down below.
3. ```javascript
   script: (function(){if(document.cookie.includes('ltoken')&&document.cookie.includes('ltuid')){const e=document.createElement('input');e.value=document.cookie,document.body.appendChild(e),e.focus(),e.select();var t=document.execCommand('copy');document.body.removeChild(e),t?alert('HoYoLAB cookie copied to clipboard'):prompt('Failed to copy cookie. Manually copy the cookie below:\n\n',e.value)}else alert('Please logout and log back in. Cookie is expired/invalid!')})();
   ```
4. Once you've successfully ran the script, click the Click here to copy! button to copy the cookie.
5. Finally, you can copy your cookie and put it inside of [helper.py](./helper.py)
6. Run the script via `python ./helper.py` and copy paste the minified token as the value for your github action secret.


The format of the credentials can be seen as the following [helper.py](./helper.py):

```python
import json
import sys
import logging

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/xxx/xxx"
HOYO_TOKENS = [
    {
        "ltoken": "xxx", # Put your ltoken here
        "ltuid": 123, # Put your ltuid here
        "games": ["gs", "hsr"], # Choose your games to sign in here
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

*games* field must be one of `(gs, hsr, hi3, zzz)`

Supports multiple tokens, in case you want to do it for multiple accounts


### Mihoyo Authentication Update

Mihoyo might have updated their authentication to use `ltuid_v2` and `ltoken_v2` instead. You can modify `HOYO_TOKENS` to change/add `enable_v2` as shown below, and use it when generating the required secrets to be passed in github's action secret

```python
HOYO_TOKENS = [
    {
        "ltoken": "xxx",
        "ltuid": 123,
        "games": ["gs", "hsr", "zzz"],
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
        "games": ["gs", "hsr", "zzz"],
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
