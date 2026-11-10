import pytest
from rest_framework.exceptions import ValidationError

from monitoring.api.serializers import StationWriteSerializer


def test_station_code_rejects_spaces():
    serializer = StationWriteSerializer()

    with pytest.raises(ValidationError):
        serializer.validate_code("Invalid code")