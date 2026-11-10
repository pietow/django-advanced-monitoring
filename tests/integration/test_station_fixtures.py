def test_station_belongs_to_user(station, user):
    assert station.owner == user