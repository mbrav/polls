import pytest
from django.urls import reverse
from polls.models import AnonUser as User


class TestAuth:

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
    def test_get_token(self, user_client):
        url = reverse('token_get')
        response = user_client.post(url)
        assert response.status_code == 200
        assert response.data.get('token')


class TestPolls:

    @pytest.mark.django_db
    def test_poll_created(self, user_unauth, poll_1, poll_2):

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

    @pytest.mark.django_db
    def test_poll_choices(
            self, user_unauth, poll_1_choices, poll_2_choices):

        url = reverse('polls-list')
        response = user_unauth.get(url)
        p_1 = response.data['results'][0]
        p_2 = response.data['results'][1]

        assert response.status_code == 200

        for c, choice in enumerate(p_1['choices']):
            assert choice['text'] == poll_1_choices[c].text

        for c, choice in enumerate(p_2['choices']):
            assert choice['text'] == poll_2_choices[c].text

    @pytest.mark.django_db
    def test_poll_my(self, user_client, user_client2, poll_1, poll_2):
        url = reverse('polls-my')
        response = user_client.get(url)
        response2 = user_client2.get(url)

        assert response.status_code == 200
        assert response2.status_code == 200
        assert len(response.data) == 1
        assert len(response2.data) == 1

    @pytest.mark.django_db
    def test_poll_are_currently_open(
            self, user_client, user_client2, poll_1, poll_2):
        url = reverse('polls-are-open')
        response = user_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 2

        url = reverse('polls-close', kwargs={'pk': poll_1.pk})
        response = user_client.post(url)
        url = reverse('polls-are-open')
        response = user_client.get(url)
        assert len(response.data) == 1

        url = reverse('polls-close', kwargs={'pk': poll_2.pk})
        response = user_client2.post(url)
        url = reverse('polls-are-open')
        response = user_client.get(url)
        assert len(response.data) == 0

    @pytest.mark.django_db
    def test_poll_close(self, user_client, poll_1):
        url = reverse('polls-close', kwargs={'pk': poll_1.pk})

        assert poll_1.is_open
        response = user_client.post(url)
        assert response.status_code == 202
        assert response.data['is_open'] == False

    @pytest.mark.django_db
    def test_poll_close_permission(self, user_client, poll_2):
        url = reverse('polls-close', kwargs={'pk': poll_2.pk})

        response = user_client.post(url)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_poll_add_choice(self, user_client, poll_1):

        text = 'New choice'
        url = reverse('polls-add-choice', kwargs={'pk': poll_1.pk})
        response = user_client.post(url, {'choice': text})

        assert response.status_code == 201

        url = reverse('polls-detail', kwargs={'pk': poll_1.pk})
        response = user_client.get(url)

        assert text == response.data['choices'][0]['text']

    @pytest.mark.django_db
    def test_poll_add_choice_permission(self, user_client, poll_2):

        text = 'New choice'
        url = reverse('polls-add-choice', kwargs={'pk': poll_2.pk})
        response = user_client.post(url, {'choice': text})

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_poll_extend(self, user_client, poll_1):

        url = reverse('polls-close', kwargs={'pk': poll_1.pk})
        response = user_client.post(url)
        assert response.data['is_open'] == False

        url = reverse('polls-extend', kwargs={'pk': poll_1.pk})
        response = user_client.post(url, {'minutes': 60})
        assert response.status_code == 202
        assert response.data['is_open']

        response = user_client.post(url, {})
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_poll_extend_permission(self, user_client, poll_2):

        url = reverse('polls-extend', kwargs={'pk': poll_2.pk})
        response = user_client.post(url, {'minutes': 60})
        assert response.status_code == 403


class TestVotes:

    @pytest.mark.django_db
    def test_votes_unauthenticated(self, user_unauth):
        url = reverse('votes-list')
        response = user_unauth.get(url)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_votes_authenticated(self, user_client):
        url = reverse('votes-list')
        response = user_client.get(url)
        assert response.status_code == 200
