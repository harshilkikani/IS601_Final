from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User, UserRole
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app

# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client, user_token, email_service):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Define user data for the test
    user_data = {
        "nickname": generate_nickname(),
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    # Send a POST request to create a user
    response = await async_client.post("/users/", json=user_data, headers=headers)
    # Asserts
    assert response.status_code == 403

# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]


@pytest.mark.asyncio
async def test_delete_user(async_client, admin_user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{admin_user.id}", headers=headers)
    assert delete_response.status_code == 204
    # Verify the user is deleted
    fetch_response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "AnotherPassword123!",
        "role": UserRole.ADMIN.name
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

@pytest.mark.asyncio
async def test_login_success(async_client, verified_user):
    # Attempt to login with the test user
    form_data = {
        "username": verified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # Check for successful login response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Use the decode_token method from jwt_service to decode the JWT
    decoded_token = decode_token(data["access_token"])
    assert decoded_token is not None, "Failed to decode token"
    assert decoded_token["role"] == "AUTHENTICATED", "The user role should be AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    form_data = {
        "username": "nonexistentuser@here.edu",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, verified_user):
    form_data = {
        "username": verified_user.email,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401
    assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_unverified_user(async_client, unverified_user):
    form_data = {
        "username": unverified_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_locked_user(async_client, locked_user):
    form_data = {
        "username": locked_user.email,
        "password": "MySuperPassword$1234"
    }
    response = await async_client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 400
    assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {admin_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client, admin_user, admin_token):
    updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client, admin_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client, manager_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client, user_token):
    response = await async_client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user

@pytest.mark.asyncio
async def test_update_profile_with_valid_data(async_client, test_user):
    token = test_user['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"first_name": "New", "last_name": "Name", "email": "newemail@example.com", "bio": "Updated bio."}
    response = await async_client.put("/users/me", json=update_data, headers=headers)
    print(f"[TEST DEBUG] status_code={response.status_code}, response_body={response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "New"
    assert data["last_name"] == "Name"
    assert data["email"] == "newemail@example.com"
    assert data["bio"] == "Updated bio."

@pytest.mark.asyncio
async def test_update_profile_with_invalid_email(async_client, test_user):
    token = test_user['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"email": "notanemail"}
    response = await async_client.put("/users/me", json=update_data, headers=headers)
    assert response.status_code == 422 or response.status_code == 400

@pytest.mark.asyncio
async def test_update_profile_with_empty_required_field(async_client, test_user):
    token = test_user['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"name": ""}
    response = await async_client.put("/users/me", json=update_data, headers=headers)
    assert response.status_code == 422 or response.status_code == 400

@pytest.mark.asyncio
async def test_update_profile_with_long_input(async_client, test_user):
    token = test_user['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    long_bio = "A" * 10000
    update_data = {"bio": long_bio}
    response = await async_client.put("/users/me", json=update_data, headers=headers)
    assert response.status_code in (200, 422, 400)

@pytest.mark.asyncio
async def test_update_profile_with_special_characters(async_client, test_user):
    token = test_user['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"bio": "!@#$%^&*()_+-=~`[]{}|;':,./<>?"}
    response = await async_client.put("/users/me", json=update_data, headers=headers)
    assert response.status_code in (200, 422)
    if response.status_code == 200:
        data = response.json()
        assert data["bio"] == "!@#$%^&*()_+-=~`[]{}|;':,./<>?"

@pytest.mark.asyncio
async def test_update_profile_with_sql_injection_attempt(async_client, test_user):
    token = test_user['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"bio": "Robert'); DROP TABLE users;--"}
    response = await async_client.put("/users/me", json=update_data, headers=headers)
    assert response.status_code in (200, 422, 400)
    if response.status_code == 200:
        data = response.json()
        assert "DROP TABLE" not in data["bio"]

@pytest.mark.asyncio
async def test_upgrade_to_professional_status_as_admin(async_client, admin_user_with_token, test_user, mocker):
    mock_send_email = mocker.patch("app.services.email_service.EmailService.send_user_email", autospec=True)
    token = admin_user_with_token['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    user_id = test_user['id']
    response = await async_client.post(f"/users/{user_id}/upgrade_professional", headers=headers)
    assert response.status_code == 200
    assert mock_send_email.called

@pytest.mark.asyncio
async def test_upgrade_to_professional_status_as_regular_user(async_client, another_user, mocker):
    """
    This test now uses a REGULAR user (not ADMIN) to ensure RBAC is enforced.
    """
    from app.models.user_model import UserRole
    # Create a regular user and get token
    from app.services.jwt_service import create_access_token
    user_id = another_user['id']
    token = create_access_token(data={"sub": user_id, "role": UserRole.AUTHENTICATED.name})
    headers = {"Authorization": f"Bearer {token}"}
    mock_send_email = mocker.patch("app.services.email_service.EmailService.send_user_email", autospec=True)
    response = await async_client.post(f"/users/{user_id}/upgrade_professional", headers=headers)
    assert response.status_code == 403
    assert not mock_send_email.called

@pytest.mark.asyncio
async def test_unauthorized_profile_update(async_client, test_user, another_user):
    token = test_user['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"first_name": "Hacker", "last_name": "McHackface"}
    response = await async_client.put(f"/users/{another_user['id']}", json=update_data, headers=headers)
    assert response.status_code in (403, 404)

@pytest.mark.asyncio
async def test_notification_sent_on_professional_status_upgrade(async_client, admin_user_with_token, test_user, mocker):
    mock_send_email = mocker.patch("app.services.email_service.EmailService.send_user_email", autospec=True)
    token = admin_user_with_token['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    user_id = test_user['id']
    response = await async_client.post(f"/users/{user_id}/upgrade_professional", headers=headers)
    assert response.status_code == 200
    assert mock_send_email.called
