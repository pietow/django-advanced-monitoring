from django.urls import reverse


def test_station_detail_requires_authentication(
    api_client,
    station,
):

    url = reverse('station-detail', args=[station.pk]) 

    response = api_client.get(url)

    assert response.status_code == 401

def test_owner_can_read_station(
        api_client,
        user,
        station,
):
    api_client.force_authenticate(user=user)
    url = reverse('station-detail', args=[station.pk]) 

    response = api_client.get(url)

    assert response.status_code == 200