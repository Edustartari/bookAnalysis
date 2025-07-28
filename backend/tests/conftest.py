import os, sys, requests, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'bookAnalysis.settings'

import django
django.setup()

import pytest  
from rest_framework.test import APIClient
  
@pytest.fixture(scope="function")  
def api_client() -> APIClient:  
    """  
    Fixture to provide an API client  
    :return: APIClient  
    """  
    yield APIClient()

