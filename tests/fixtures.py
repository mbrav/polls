import pytest


def ip_headers(ip: str):
    header = {
        'HTTP_X_FORWARDED_FOR': ip,
        'REMOTE_ADDR': ip,
    }
    return header


@pytest.fixture
def user(django_user_model):
    from polls.models import AnonUser as User
    return User.objects.create(ip_address='127.127.127.1')


@pytest.fixture
def user2(django_user_model):
    from polls.models import AnonUser as User
    return User.objects.create(ip_address='127.127.127.2')


@pytest.fixture
def token(user):
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def token2(user2):
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=user2)
    return token


@pytest.fixture
def user_unauth():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient
    user_ip = token.user.ip_address
    client = APIClient(**ip_headers(user_ip))
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.fixture
def user_client2(token2):
    from rest_framework.test import APIClient
    user_ip = token2.user.ip_address
    client = APIClient(**ip_headers(user_ip))
    client.credentials(HTTP_AUTHORIZATION=f'Token {token2.key}')
    return client


@pytest.fixture
def poll_1(user):
    from polls.models import Poll
    return Poll.objects.create(
        owner=user, name='poll_1', description='Best politicians')


@pytest.fixture
def poll_2(user2):
    from polls.models import Poll
    return Poll.objects.create(
        owner=user2, name='poll_2', description='Best people')


@pytest.fixture
def poll_3(user):
    from polls.models import Poll
    return Poll.objects.create(
        owner=user, type='2', name='poll_3', description='Many choices')


@pytest.fixture
def poll_4(user):
    from polls.models import Poll
    return Poll.objects.create(
        owner=user, type='3', name='poll_4', description='Psychiatrist Visit')


@pytest.fixture
def poll_1_choices(poll_1):
    from polls.models import Choice
    c1 = Choice.objects.create(poll=poll_1, text='George Bush')
    c2 = Choice.objects.create(poll=poll_1, text='Angela Merkel')
    c3 = Choice.objects.create(poll=poll_1, text='Leonid Breshnev')
    return (c1, c2, c3)


@pytest.fixture
def poll_2_choices(poll_2):
    from polls.models import Choice
    c1 = Choice.objects.create(poll=poll_2, text='Steven Hawking')
    c2 = Choice.objects.create(poll=poll_2, text='Immanuel Kant')
    return (c1, c2)


@pytest.fixture
def poll_3_choices(poll_3):
    from polls.models import Choice
    c1 = Choice.objects.create(poll=poll_3, text='Plato')
    c2 = Choice.objects.create(poll=poll_3, text='Aristotle')
    return (c1, c2)


@pytest.fixture
def poll_3_votes(user, user2, poll_3, poll_3_choices):
    from polls.models import Vote
    v1 = Vote.objects.create(user=user, poll=poll_3,
                             choice=poll_3_choices[0])
    v2 = Vote.objects.create(user=user2, poll=poll_3,
                             choice=poll_3_choices[0])
    v3 = Vote.objects.create(user=user2, poll=poll_3,
                             choice=poll_3_choices[1])
    return (v1, v2, v3)


@pytest.fixture
def poll_4_answers(user, user2, poll_4):
    from polls.models import Answer
    a1 = Answer.objects.create(user=user2, poll=poll_4,
                             text='Call suicide prevention hotline')
    return (a1,)
