from datetime import timedelta, timezone, datetime
import re
from typing import Final

from rest_framework import serializers


class TimezoneField(serializers.CharField):
    TIMEZONE_REGEX_PATTERN: Final[re.Pattern] = re.compile(
        '^[+-](?:2[0-3]|[01][0-9]):[0-5][0-9]$'
    )

    default_error_messages = serializers.CharField.default_error_messages | {
        'invalid_format': (
            f"Timezone must be in the format ±hh:mm (regex: "
            f"{TIMEZONE_REGEX_PATTERN.pattern})"
        )
    }

    def to_internal_value(self, data):
        if not re.match(self.TIMEZONE_REGEX_PATTERN, data):
            self.fail('invalid_format')
        sign = 1 if data[0] == '+' else -1
        hours, minutes = map(int, data[1:].split(':'))
        offset = timedelta(hours=hours * sign, minutes=minutes * sign)
        return timezone(offset)

    def to_representation(self, value: timedelta | timezone):
        if isinstance(value, timezone):
            value: timedelta = datetime.now(value).utcoffset()
        total_minutes = value.total_seconds() / 60
        sign = '+' if total_minutes >= 0 else '-'
        hours, minutes = divmod(abs(int(total_minutes)), 60)
        return f"{sign}{hours:02}:{minutes:02}"
