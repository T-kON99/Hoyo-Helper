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
export 'HOYO_TOKENS = "<above token in string format>"'
```

### Discord Webhook

```bash
export 'DISCORD_WEBHOOK = "<your_webhook_discord_channel_here>"'
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

1. Utilizes github workflows to run the job.