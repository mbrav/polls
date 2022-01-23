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
        p_1 = response.data.get('results')[0]
        p_2 = response.data.get('results')[1]

        assert response.status_code == 200

        assert poll_1.is_open
        assert poll_1.name == p_1['name']
        assert p_1['is_open']
        assert poll_1.description == p_1['description']

        assert poll_2.is_open
        assert poll_2.name == p_2['name']
        assert p_2['is_open']
        assert poll_2.description == p_2['description']

    def test_poll_detail(self, user_unauth, poll_1):
        url = reverse('polls-detail', kwargs={'pk': poll_1.id})
        response = user_unauth.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_poll_choices(
            self, user_unauth, poll_1_choices, poll_2_choices):

        url = reverse('polls-list')
        response = user_unauth.get(url)
        p_1 = response.data.get('results')[0]
        p_2 = response.data.get('results')[1]

        assert response.status_code == 200

        for c, choice in enumerate(p_1['choices']):
            assert choice.get('text') == poll_1_choices[c].text

        for c, choice in enumerate(p_2['choices']):
            assert choice.get('text') == poll_2_choices[c].text

    @pytest.mark.django_db
    def test_poll_patch(self, user_client, poll_1):
        url = reverse('polls-detail', kwargs={'pk': poll_1.pk})

        response = user_client.get(url)

        new_name = 'New Poll Name'
        name = response.data.get('name')
        response = user_client.patch(url, {'name': new_name})

        assert response.data.get('name') != name
        assert response.data.get('name') == new_name
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_poll_delete(self, user_client, poll_1):
        url = reverse('polls-detail', kwargs={'pk': poll_1.pk})

        response = user_client.delete(url)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_poll_delete_permission(self, user_client, poll_2):
        url = reverse('polls-detail', kwargs={'pk': poll_2.pk})

        response = user_client.delete(url)
        assert response.status_code != 204
        assert response.status_code == 403

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
        assert response.data.get('is_open') is False

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

        assert text == response.data.get('choices')[0]['text']

    @pytest.mark.django_db
    def test_poll_add_choice_duplicate(
            self, user_client, poll_1, poll_1_choices):

        text = poll_1_choices[0].text
        url = reverse('polls-add-choice', kwargs={'pk': poll_1.pk})
        response = user_client.post(url, {'choice': text})

        assert response.status_code == 400

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
        assert response.data.get('is_open') is False

        url = reverse('polls-extend', kwargs={'pk': poll_1.pk})
        response = user_client.post(url, {'minutes': 60})
        assert response.status_code == 202
        assert response.data.get('is_open')

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

    @pytest.mark.django_db
    def test_vote_detail(self, user_client, poll_3_votes):
        url = reverse('votes-detail', kwargs={'pk': poll_3_votes[0].id})
        response = user_client.get(url)
        assert response.status_code == 200

    def test_vote_detail_permission(self, user_client2, poll_3_votes):
        url = reverse('votes-detail', kwargs={'pk': poll_3_votes[0].id})
        response = user_client2.get(url)
        assert response.status_code != 200
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_vote_create(self, user_client, poll_1, poll_1_choices):

        url = reverse('votes-list')

        choice = poll_1_choices[0].id
        response = user_client.post(
            url, {'poll': poll_1.pk, 'choice': choice})
        assert response.status_code == 201

        choice2 = poll_1_choices[1].id
        response = user_client.post(
            url, {'poll': poll_1.pk, 'choice': choice2})
        assert response.status_code != 201

        url = reverse('votes-list')
        response = user_client.get(url)
        assert response.data[0].get('choice') == choice

    @pytest.mark.django_db
    def test_vote_create_closed(
            self, user_client, poll_1, poll_1_choices):

        url = reverse('polls-close', kwargs={'pk': poll_1.pk})

        assert poll_1.is_open
        response = user_client.post(url)

        url = reverse('votes-list')

        choice = poll_1_choices[0].id
        response = user_client.post(
            url, {'poll': poll_1.pk, 'choice': choice})
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_vote_multiple_create(self, user_client, poll_3, poll_3_choices):

        url = reverse('votes-list')

        choice = poll_3_choices[0].id
        response = user_client.post(
            url, {'poll': poll_3.pk, 'choice': choice})
        assert response.status_code == 201

        response = user_client.post(
            url, {'poll': poll_3.pk, 'choice': choice})
        assert response.status_code != 201

        choice2 = poll_3_choices[1].id
        response = user_client.post(
            url, {'poll': poll_3.pk, 'choice': choice2})
        assert response.status_code == 201

        url = reverse('votes-list')
        response = user_client.get(url)
        assert response.data[0].get('choice') == choice
        assert response.data[1].get('choice') == choice2

    @pytest.mark.django_db
    def test_vote_patch(self, user_client, poll_3, poll_3_choices):

        url = reverse('votes-list')
        choice = poll_3_choices[0].id
        choice2 = poll_3_choices[1].id

        response = user_client.post(
            url, {'poll': poll_3.pk, 'choice': choice})

        created_choice = response.data

        url = reverse('votes-detail', kwargs={'pk': created_choice['id']})
        response = user_client.patch(
            url, {'choice': choice2})

        assert response.data.get('choice') != created_choice
        assert response.data.get('choice') == choice2

    @pytest.mark.django_db
    def test_vote_delete(self, user_client, poll_3_votes):
        url = reverse('votes-detail', kwargs={'pk': poll_3_votes[0].id})

        response = user_client.delete(url)
        assert response.status_code == 204

        response = user_client.get(url)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_vote_delete_permission(self, user_client2, poll_3_votes):
        url = reverse('polls-detail', kwargs={'pk': poll_3_votes[0].id})

        response = user_client2.delete(url)
        assert response.status_code != 204
        assert response.status_code == 403


class TestAnswers:

    @pytest.mark.django_db
    def test_answers_unauthenticated(self, user_unauth):
        url = reverse('answers-list')
        response = user_unauth.get(url)
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_answers_authenticated(self, user_client):
        url = reverse('answers-list')
        response = user_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_answer_detail(self, user_client2, poll_4_answers):
        url = reverse('answers-detail', kwargs={'pk': poll_4_answers[0].id})
        response = user_client2.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_answer_detail_permission(self, user_client, poll_4_answers):
        url = reverse('answers-detail', kwargs={'pk': poll_4_answers[0].id})
        response = user_client.get(url)
        assert response.status_code != 200
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_answer_create(self, user_client, poll_4):

        url = reverse('answers-list')

        new_answer = 'Test answer'
        response = user_client.post(
            url, {'poll': poll_4.pk, 'text': new_answer})
        assert response.status_code == 201

        response = user_client.post(
            url, {'poll': poll_4.pk, 'text': new_answer})
        assert response.status_code != 201

        url = reverse('answers-list')
        response = user_client.get(url)
        assert response.data[0].get('text') == new_answer

    @pytest.mark.django_db
    def test_answer_create_closed(
            self, user_client, poll_4):

        url = reverse('polls-close', kwargs={'pk': poll_4.pk})

        assert poll_4.is_open
        response = user_client.post(url)

        url = reverse('votes-list')
        new_answer = 'Test answer'
        response = user_client.post(
            url, {'poll': poll_4.pk, 'text': new_answer})
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_answer_patch(self, user_client, poll_4):

        url = reverse('answers-list')
        new_answer = 'Test answer'

        response = user_client.post(
            url, {'poll': poll_4.pk, 'text': new_answer})

        created_answer = response.data
        edit_answer = 'Test answer edited'

        url = reverse('answers-detail', kwargs={'pk': created_answer['id']})
        response = user_client.patch(
            url, {'text': edit_answer})

        assert response.data.get('text') != created_answer
        assert response.data.get('text') == edit_answer

    @pytest.mark.django_db
    def test_answer_delete(self, user_client2, poll_4, poll_4_answers):
        url = reverse('answers-detail', kwargs={'pk': poll_4_answers[0].id})

        response = user_client2.delete(url)
        assert response.status_code == 204

        response = user_client2.get(url)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_answer_delete_permission(self, user_client, poll_4_answers):
        url = reverse('answers-detail', kwargs={'pk': poll_4_answers[0].id})

        response = user_client.delete(url)
        assert response.status_code != 204
        assert response.status_code == 403
