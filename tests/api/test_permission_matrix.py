import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    ("role", "method", "expected_status"),
    [
        ("anonymous", "get", 401),
        ("other", "get", 200),
        ("other", "patch", 403),
        ("owner", "patch", 200),
        ("staff", "patch", 200),
        ("other", "delete", 403),
        ("owner", "delete", 204),
        ("staff", "delete", 204),
    ],
)
def test_station_permission_matrix(
    api_client,
    user,
    other_user,
    staff_user,
    station,
    role,
    method,
    expected_status,
):
    users_by_role = {
        "anonymous": None,
        "other": other_user,
        "owner": user,
        "staff": staff_user,
    }

    selected_user = users_by_role[role]

    if selected_user is not None:
        api_client.force_authenticate(
            user=selected_user,
        )

    url = reverse(
        "station-detail",
        args=[station.pk],
    )

    if method == "get":
        response = api_client.get(url)

    elif method == "patch":
        response = api_client.patch(
            url,
            {"name": "Permission Matrix"},
            format="json",
        )

    elif method == "delete":
        response = api_client.delete(url)

    else:
        pytest.fail(f"Unbekannte HTTP-Methode: {method}")

    assert response.status_code == expected_status
