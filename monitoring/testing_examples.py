VALID_QUALITY_FLAGS = {
    "valid",
    "suspect",
    "invalid",
}


def is_valid_quality_flag(value: str) -> bool:
    """Return whether the value is a supported quality flag."""
    return value in VALID_QUALITY_FLAGS
