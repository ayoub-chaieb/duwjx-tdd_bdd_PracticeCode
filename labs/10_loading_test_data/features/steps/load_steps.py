# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Pet Steps
Steps file for Pet.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

# Load data here
@given("the following pets")
def step_impl(context):
    """Refresh all Pets in the database"""
    # List all pets and delete them one by one
    response = requests.get(f"{context.base_url}/pets")
    assert 200 == response.status_code
    for pet in response.json():
        response = requests.delete(f"{context.base_url}/pets/{pet['id']}")
        assert 204 == response.status_code
    
    # load the database with new pets
    for row in context.table:
        payload= {}
        
        payload["name"] = row["name"]
        payload["category"] = row["category"]
        payload["available"] = row["available"] in ["True", "true", 1, ]
        payload["gender"] = row["gender"]
        payload["birthday"] = row["birthday"]
        
        response = requests.post(f"{context.base_url}/pets", json=payload)
        assert 201 == response.status_code
