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
