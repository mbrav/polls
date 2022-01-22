import pytest
from django.urls import reverse
from polls.models import AnonUser as User


class TestAPI:

    @pytest.mark.django_db
    def test_api_root(self, user_unauth):
        url = reverse('api-root')
        response = user_unauth.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_count(self, ):
        assert User.objects.count() == 0

    @pytest.mark.django_db
    def test_users_created(self, user, user2, user_client, user_client2):
        assert User.objects.filter(ip_address=user.ip_address).exists()
        assert user.ip_address == user_client.defaults['REMOTE_ADDR']
        assert User.objects.filter(ip_address=user2.ip_address).exists()
        assert user2.ip_address == user_client2.defaults['REMOTE_ADDR']
        assert User.objects.count() == 2

    @pytest.mark.django_db
    def test_api_unauthenticated(self, user_unauth):
        url = reverse('votes-list')
        response = user_unauth.get(url)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_api_authenticated(self, user_client):
        url = reverse('votes-list')
        response = user_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_token(self, user_client):
        url = reverse('token_get')
        response = user_client.post(url)
        assert response.status_code == 200
        assert response.data.get('token')


class TestPolls:

    @pytest.mark.django_db
    def test_poll_created(self, user_unauth, poll_1, poll_2):

        poll_1_choices = poll_1.pop()
        poll_1 = poll_1.pop()
        poll_2_choices = poll_2.pop()
        poll_2 = poll_2.pop()

        url = reverse('polls-list')
        response = user_unauth.get(url)
        p_1 = response.data['results'][0]
        p_2 = response.data['results'][1]

        assert response.status_code == 200

        assert poll_1.is_open
        assert poll_1.name == p_1['name']
        assert p_1['is_open']
        assert poll_1.description == p_1['description']

        assert poll_2.is_open
        assert poll_2.name == p_2['name']
        assert p_2['is_open']
        assert poll_2.description == p_2['description']

        for c, choice in enumerate(p_1['choices']):
            assert choice['text'] == poll_1_choices[c].text

        for c, choice in enumerate(p_2['choices']):
            assert choice['text'] == poll_2_choices[c].text
