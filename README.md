[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python)](https://www.python.org)
[![build](https://github.com/leandcesar/bobotinho-bot/workflows/CI/badge.svg)](https://github.com/leandcesar/bobotinho-bot/actions/workflows/ci.yml)
[![UptimeRobot](https://img.shields.io/uptimerobot/status/m788541737-d1097381d469c36beb1e16b3)](https://stats.uptimerobot.com/EQQpJSWDE5/788541737)
[![codecov](https://codecov.io/gh/leandcesar/bobotinho-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/leandcesar/bobotinho-bot)
[![License](https://img.shields.io/badge/license-AGPL%20v3-yellow.svg)](https://github.com/leandcesar/bobotinho-bot/blob/main/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Bobotinho Bot
Main repository for the chatbot Bobotinho.

## âšī¸ Introduction
Twitch chatbot with entertainment commands.

### âđģ Technologies
- Concurrent code with [**asyncio**](https://docs.python.org/3/library/asyncio.html)
- Asynchronous HTTP Client/Server with [**AIOHTTP**](https://docs.aiohttp.org/en/stable/)
- Relational Database with [**PostgreSQL**](https://www.postgresql.org/)
- In-memory data structure store with [**Redis**](https://redis.io/)
- Asynchronous ORM (Object Relational Mapper) with [**Tortoise**](https://tortoise-orm.readthedocs.io/)
- Asynchronous wrapper around the Twitch API with [**TwitchIO 2**](https://twitchio.readthedocs.io/en/latest/index.html)

### đ Services
- Application stability monitor with [**Bugsnag**](https://www.bugsnag.com/)
- Chatbot Analytics with [**Dashbot**](https://www.dashbot.io/)
- Uptime monitoring service with [**UptimeRobot**](https://uptimerobot.com/)
- Coverage reports with [**Codecov**](https://about.codecov.io/)

### âđ§° Dev tools
- Code formatter with [**Black**](https://github.com/psf/black)
- Style guide with [**flake8**](https://flake8.pycqa.org/en/latest/)
- Run containers with [**Docker**](https://www.docker.com/) and [**Docker Compose**](https://docs.docker.com/compose/)
- Run GitHub Actions locally with [**act**](https://github.com/nektos/act)
- Pre-commit hooks with [**pre-commit**](https://pre-commit.com/)

## đ Getting Started
It is assumed that you have:
- [**Twitch**](https://twitch.tv/) account for your bot.
- [**Python 3.8+**](https://www.python.org/) installed.
- [**Pip**](https://pip.pypa.io/en/stable/) installed.

```bash
$ python3 --version
$ pip3 --version
```

### đ Access Token

Visit [**Token Generator**](https://twitchtokengenerator.com/) and select the "Bot Chat Token". After selecting this you can copy your "Access Token" somewhere safe.

### âī¸ Configuring

After clone this repo, create `.env` file in your `/bobotinho-bot` directory. Add the access token from above and dev nick after the `=`. Optionally add and fill other env vars (see `.env.template`).

```
ACCESS_TOKEN=your-token-here
DEV_NICK=your-twitch-nick
```

### âļī¸ Run 

#### đ  Option 1: locally

The standard library as of Python 3.3 comes with a concept called "Virtual Environment"s to keep libraries from polluting system installs or to help maintain a different version of libraries than the ones installed on the system.

Execute the following commands in your `/bobotinho-bot` directory:

```bash
$ python3.8 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ env/bin/python bot.py
```

#### đ Option 2: with `docker`

It is assumed that you have [**Docker**](https://www.docker.com/) installed.

```bash
$ docker --version
```

Otherwise, you can download and install Docker [**here**](https://docs.docker.com/get-docker/).

Execute the following commands in your `/bobotinho-bot` directory:

```bash
$ docker build -t bobotinho-bot .
$ docker run bobotinho-bot
```

#### đŗ Option 3: with `docker-compose`

It is assumed that you have [**Docker**](https://www.docker.com/) and **Docker Compose** installed.

```bash
$ docker --version
$ docker-compose --version
```

Otherwise, you can download and install Docker Compose [**here**](https://docs.docker.com/compose/install/).

Execute the following commands in your `/bobotinho-bot` directory:

```bash
$ docker-compose up --build
```

> *Use `--build` flag only on the first run*

### đ Use

Go to [twitch.tv/`DEV_NICK`](https://twitch.tv/) and send `%ping`.
