from datetime import datetime, timezone


class TimezoneConverter:
    class NotUTCException(Exception):
        def __init__(self, message="The time must be in UTC"):
            super().__init__(message)

    def convert_to_utc(self, dt: datetime) -> datetime:
        utc_dt = dt.astimezone(timezone.utc)
        return utc_dt

    def convert_from_utc(self, dt: datetime, target_timezone: timezone) -> datetime:
        if dt.tzinfo and dt.tzinfo != timezone.utc:
            raise self.NotUTCException
        target_dt = dt.astimezone(target_timezone)
        return target_dt
