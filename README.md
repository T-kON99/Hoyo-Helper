# Hoyo Helper

This is a hoyo helper intended to help user check-ins automatically

## Setting Up

### Hoyo Credentials

You require the cookies containing `ltuid` and `ltoken`, which the format of the token can be seen as the following:

```python
HOYO_TOKENS = [
    {
        "ltoken": "xxx",
        "ltuid": 000,
        "games": ["gs", "hsr"],
    },
]
```

Supports multiple tokens, in case you want to do it for multiple accounts...

*games* field must be one of `(gs, hsr, hi3)`

```bash
echo 'HOYO_TOKENS = "<above token>"' >> secret.py
```

### Discord Webhook

```bash
echo 'DISCORD_WEBHOOK = "<your_webhook_discord_channel_here>"' >> secret.py
```

### Usage

```bash
git clone https://github.com/T-kON99/Hoyo-Helper.git
```

### Installating Dependencies

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Running

```bash
python main.py
```

### Footnotes

1. You can use `cron` job to schedule this at a regular interval. Alternatively you can set up Google pub/sub API to `watch` your gmail instead, but that is not what this project is for.
2. Alternatively you can use [pythonanywhere](https://www.pythonanywhere.com/) to host this project and run `./run.sh` instead. Do set the permission to be an executeable script with `chmod +x ./run.sh`. 
3. Replace the dir specified in `./run.sh` to your respective dir.