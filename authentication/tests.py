import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import CustomUser

@pytest.mark.django_db
class TestAuthenticationViews:

    def setup_method(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'teste123'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)
        self.token_url = reverse('authentication:token_obtain_pair')
        self.refresh_url = reverse('authentication:token_refresh')
        self.verify_url = reverse('authentication:token_verify')

    def test_token_obtain_pair_success(self):
        response = self.client.post(self.token_url, {
            'username': self.username,
            'password': self.password
        })

        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_token_obtain_pair_invalid_credentials(self):
        response = self.client.post(self.token_url, {
            'username': 'wrong_user',
            'password': 'wrong_password'
        })

        assert response.status_code == 401
        assert 'access' not in response.data
        assert 'refresh' not in response.data

    def test_token_refresh_success(self):
        response = self.client.post(self.token_url, {
            'username': self.username,
            'password': self.password
        })
        refresh_token = response.data['refresh']

        response = self.client.post(self.refresh_url, {'refresh': refresh_token})

        assert response.status_code == 200
        assert 'access' in response.data

    def test_token_verify_success(self):
        response = self.client.post(self.token_url, {
            'username': self.username,
            'password': self.password
        })
        access_token = response.data['access']

        response = self.client.post(self.verify_url, {'token': access_token})

        assert response.status_code == 200