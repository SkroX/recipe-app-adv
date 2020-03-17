from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_success(self):

        info = {
            'email': 'abc123@gmail.com',
            'password': 'abc123',
            'name': 'mai'
        }

        res = self.client.post(CREATE_USER_URL, info)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(info['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):

        info = {'email': 'abc123', 'password': 'abc1123'}
        create_user(**info)

        res = self.client.post(CREATE_USER_URL, info)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):

        info = {'email': 'abc123', 'password': 'a'}
        res = self.client.post(CREATE_USER_URL, info)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=info['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):

        info = {'email': 'abc123', 'password': 'abc123'}
        create_user(**info)
        res = self.client.post(TOKEN_URL, info)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):

        create_user(email='abc123', password='abc123')
        info = {'enail': 'abc123', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, info)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):

        info = {'email': 'abc1230', 'password': 'abc123'}
        res = self.client.post(TOKEN_URL, info)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_field(self):

        res = self.client.post(TOKEN_URL, {'email': 'ad', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def tesr_retrieve_user_unauthorized(self):

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAOTHORIZED)


class PrivateUserApiTest(TestCase):

    def setUp(self):

        self.user = create_user(
            email='abc123@gmail.com',
            password='abc123',
            name='mai'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profle(self):

        info = {'name': 'new name', 'password': 'newpassword'}

        res = self.client.patch(ME_URL, info)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, info['name'])
        self.assertTrue(self.user.check_password(info['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
