import requests
import random

def random_digits(digits: int) -> str:
    """
    Generate a string of random digits of a specified length.
    """
    # In Python, '^' is the bitwise XOR operator, not exponentiation.
    # For exponentiation, use '**'.
    lower = 10 ** (digits - 1)
    upper = (10 ** digits) - 1
    return str(random.randint(lower, upper))

def test_successful_registration():
    """
    Test a successful registration on https://reqres.in/
    by sending an email and a generated password.
    """
    url = "https://reqres.in/api/register"
    payload = {
        "email": "eve.holt@reqres.in",
        "password": random_digits(8)  # Generate an 8-digit password
    }

    response = requests.post(url=url, json=payload)
    # Check the status code is 200 (OK)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    response_json = response.json()

    # Check if "token" is present in the response
    assert "token" in response_json, "Response JSON should contain 'token'"
    # Optionally check that token is a string
    assert isinstance(response_json["token"], str), "Token should be a string"

    print("test_successful_registration passed!")

def test_unsuccessful_registration():
    """
    Test an unsuccessful registration on https://reqres.in/
    by omitting the 'password' field.
    """
    url = "https://reqres.in/api/register"
    payload = {
        "email": "testemail@tytest.com"
        # no password included
    }

    response = requests.post(url=url, json=payload)
    # The API should return 400 (Bad Request) if password is missing
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    response_json = response.json()

    # Check for an error message in the response
    # For Reqres, the missing password error is typically: {"error": "Missing password"}
    # You can update the assertion based on the actual response from the API.
    assert "error" in response_json, "Response JSON should contain 'error'"
    assert "Missing password" in response_json["error"], "Expected 'Missing password' in error message"

    print("test_unsuccessful_registration passed!")

if __name__ == "__main__":
    test_successful_registration()
    test_unsuccessful_registration()