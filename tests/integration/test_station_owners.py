from monitoring.models import Station



def test_stations_have_different_owners(
    station, other_station  
):
    
    assert station.owner_id != other_station.owner_id
    assert station.code != other_station.code
    assert Station.objects.filter(
        pk__in=[station.pk, other_station.pk]
    ).count() == 2