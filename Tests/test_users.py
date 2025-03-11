import requests
import json
import jsonpath

baseUrl = "https://reqres.in/"

def test_fetch_user():
    path = "api/users/2"
    response = requests.get(url=baseUrl + path)

    # Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Convert response to JSON
    response_json = response.json()

    # Extract fields using jsonpath
    first_name = jsonpath.jsonpath(response_json, '$.data.first_name')
    user_id = jsonpath.jsonpath(response_json, '$.data.id')

    # Verify jsonpath calls succeeded
    assert first_name is not False, "No match found for $.data.first_name"
    assert user_id is not False, "No match found for $.data.id"

    # Validate the fields
    assert first_name[0] == "Janet", f"Expected 'Janet', got {first_name[0]}"
    assert user_id[0] == 2, f"Expected 2, got {user_id[0]}"

    print("test_fetch_user passed!")

def test_create_delete_user():
    # Safely open and parse JSON from file
    with open("TestData/user.json", "r") as file:
        input_data = json.load(file)

    path = "api/users"
    # Send POST request with the parsed JSON data
    response = requests.post(url=baseUrl + path, json=input_data)

    # Ensure user creation returns 201
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Convert response to JSON
    response_json = response.json()

    # Extract user ID from response
    created_id = jsonpath.jsonpath(response_json, '$.id')
    assert created_id is not False, "No match found for $.id"

    # Convert the ID list element to string for the DELETE endpoint
    user_id_str = str(created_id[0])

    # Perform DELETE request
    delete_response = requests.delete(url=baseUrl + "api/users/" + user_id_str)

    # Ensure user deletion returns 204
    assert delete_response.status_code == 204, f"Expected 204, got {delete_response.status_code}"

    print("test_create_delete_user passed!")

if __name__ == "__main__":
    test_fetch_user()
    test_create_delete_user()
