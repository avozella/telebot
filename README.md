# Telebot

## Before install
Previously you have to add your token bot on /src/credentials.py

## Install locally

On terminal, run:
```bash
pip install -r requirements.txt
python /src/app.py
```
## Build with Docker
```bash
"docker build -t imagename:tag .
```
## Run image
```bash
docker run -d imagename:tag
```

## Checklist

- [x] Template with Docker
- [ ] Integration with Github Actions
- [ ] Integration with Trend API
- [ ] Integration with CVE feeds