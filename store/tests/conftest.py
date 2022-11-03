from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


# api_client.force_authenticate(user=User(is_staff=True))

@pytest.fixture
def api_client():
	return APIClient()


@pytest.fixture
def authenticate_user(api_client):
	def do_authenticate_user(is_staff=False):
		api_client.force_authenticate(user=User(is_staff=is_staff))
	return do_authenticate_user	