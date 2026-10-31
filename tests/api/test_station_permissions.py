import pytest
from django.urls import reverse


def test_owner_can_patch_station(
    api_client,
    user,
    station,
):
    api_client.force_authenticate(
        user=user,
    )

    url = reverse(
        "station-detail",
        args=[station.pk],
    )

    response = api_client.patch(
        url,
        {"name": "Changed by owner"},
        format="json",
    )

    assert response.status_code == 200


def test_other_user_cannot_patch_station(
    api_client,
    other_user,
    station,
):
    api_client.force_authenticate(
        user=other_user,
    )

    url = reverse(
        "station-detail",
        args=[station.pk],
    )

    response = api_client.patch(
        url,
        {"name": "Changed by other user"},
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.parametrize(
    ("role", "method", "expected_status"),
    [
        ("anonymous", "get", 401),
        ("other", "get", 200),
        ("other", "patch", 403),
        ("owner", "patch", 200),
        ("staff", "patch", 200),
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

    else:
        pytest.fail(f"Unbekannte HTTP-Methode: {method}")

    assert response.status_code == expected_status

