[![Django and Pytest CI](https://github.com/mbrav/polls/actions/workflows/django.yml/badge.svg)](https://github.com/mbrav/polls/actions/workflows/django.yml)
[![wakatime](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/6f9b9719-dd0c-4d89-a5fa-709edfe36471.svg)](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/6f9b9719-dd0c-4d89-a5fa-709edfe36471)

# polls

Polls is an a REST Api application that allows users to anonymously create polls and votes. Authentication is implemented using Tokens that are generated for a custom _AnonUser_ model that uses users IPv4 addresses that are hashed on the server using SHA384 hashing algorithm. **Do not rely on this approach since it is not secure** and can take a hacker less than a minute to go through all 4'294'967'296 IPv4 address combinations. It is done purely for educational purposes.

### To improve

-   [ ] [#1](https://github.com/mbrav/polls/issues/1) Configure app for IPv6 address use only
-   [ ] [#2](https://github.com/mbrav/polls/issues/2) Hash IP addresses on the backend side instead of storing addresses in clear text
-   [ ] [#3](https://github.com/mbrav/polls/issues/3) Pytest coverage

## Instructions

```bash
$ git clone https://github.com/mbrav/polls.git
$ cd heifmgur
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

Setup an admin user (not required):

```bash
$ python manage.py createsuperuser
```

Run server

```bash
$ python manage.py runserver
```

Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for a detailed ReDoc API schema description
