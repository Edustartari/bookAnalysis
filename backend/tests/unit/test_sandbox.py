import os, sys, requests, json
import pytest
from backend.views import *
from rest_framework.test import APIClient

client = APIClient()

# Use assert to define if result is correct
def test_1():
    assert True == True

# Use fixtures for mock data
@pytest.fixture
def fixture_example():
    payload = 'test'
    return payload
def test_2(fixture_example):
    assert edu_test() == fixture_example

# Use this decorator to skip this test
@pytest.mark.skip(reason='No way to test it')
def test_3():
    assert 1 == 1

# Pytest allows you to parametrize your test functions to run multiple test cases with different inputs:
# (1,2): means 1 is the input and 2 is the expected result
@pytest.mark.parametrize("input, expected", [(1, 2), (2, 4), (3, 6)])
def test_4(input, expected):
    result = input * 2
    assert result == expected

# Use client to mock API requests
# The @pytest.mark.django_db decorator is used to ensure that the test runs in a database transaction
# so that any changes made during the test are rolled back after the test is complete.
# @pytest.mark.django_db
# def test_view():
#     response = client.get('/pilots-complete-info')
#     json_data = json.loads(response.content)
#     # Check if response was successful
#     assert response.status_code == 200
#     # Include a comment after a comma (optional)
#     assert 'drivers' in json_data, f"json_data don't possess drivers key"


