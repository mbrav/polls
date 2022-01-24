[![Django and Pytest CI](https://github.com/mbrav/polls/actions/workflows/django.yml/badge.svg)](https://github.com/mbrav/polls/actions/workflows/django.yml)
[![wakatime](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/6f9b9719-dd0c-4d89-a5fa-709edfe36471.svg)](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/6f9b9719-dd0c-4d89-a5fa-709edfe36471)

# polls (Django 2.2.10 version)

Polls is an a REST Api application that allows users to anonymously create polls and votes. Authentication is implemented using Tokens that are generated for a custom _AnonUser_ model that uses users IPv4 addresses that are hashed on the server using SHA384 hashing algorithm. **Do not rely on this approach since it is not secure** and can take a hacker less than a minute to go through all 4'294'967'296 IPv4 address combinations. It is done purely for educational purposes.

### Poll types

The API supports three types of polls:

1. Choice poll
2. Multiple choice poll
3. Answer cased poll

The API enforces a rule so that answer based pools cannot accept poll votes, or vice versa. This rule however is not enforced at the database model level.

## Instructions

```bash
$ git clone https://github.com/mbrav/polls.git
$ cd polls
```

Setup a local python environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dependencies with poetry:

```bash
$ poetry install
```

Setup Django database and migrations:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

Load fixture data

```bash
$ python manage.py loaddata base/fixtures/dump.json
```

Run server

```bash
$ python manage.py runserver
```

Go to [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)

### Default user data from fixture `dump.json`:

Usernames are set based on the first 30 symbols of their IP address SHA384 hash:

-   Admin User
    -   username: `54580887f3f91d797f39d14c9d7a16`
    -   Token `4e11f089cb23d74115fec917e9f7236b11b22926`
    -   Ip address: `0.0.0.0`
-   Regulat User
    -   username: `e9568e3cf2427b7fa3cb353d86ca94`
    -   Token `7d82a5129acb41617389ebd7ae1d8abd1fcd588f`
    -   Ip address: `127.0.0.1`
