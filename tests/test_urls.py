import pytest

# https://pytest-django.readthedocs.io/en/latest/database.html
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("route, status_code", [
    ("/", 200),
    ("/about/", 200),
    ("/contact-us/", 200),
    ("/social/", 200),
    ("/accounts/login/", 200),
    ("/accounts/logout/", 302),
    ("/accounts/profile/", 302),
    ("/search/?keyword=test", 200),
    ("/all-items/", 302),
    ("/add/", 302),
])
def test_routes(client, route, status_code):
    response = client.get(route)
    assert response.status_code == status_code
