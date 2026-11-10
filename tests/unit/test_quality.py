from monitoring.testing_examples import is_valid_quality_flag


def test_valid_quality_flag_is_valid():
    # Arrange
    value = "valid"

    # Act
    result = is_valid_quality_flag(value)

    # Assert
    assert result is True