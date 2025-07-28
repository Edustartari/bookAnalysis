import os, sys, requests, json
import pytest
from backend.views import *
from rest_framework.test import APIClient

client = APIClient()

def test_index():
    response = client.get('')
    assert response.status_code == 200