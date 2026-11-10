import pytest
from monitoring.testing_examples import is_valid_quality_flag


@pytest.mark.parametrize(("value", "expected"), [("valid", True), ("unkown", False)])
def test_valid_quality_flag_is_valid(value, expected):
    assert is_valid_quality_flag(value) is expected
