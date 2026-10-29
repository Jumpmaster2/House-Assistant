"""Decision for the unchanged room temperature repair."""


def sensor_is_stale(age_seconds: float, hours: float, valid: bool) -> bool:
    """A valid reading is stale once the configured age is reached; zero disables it."""
    return bool(valid and hours > 0 and age_seconds >= hours * 3600)
