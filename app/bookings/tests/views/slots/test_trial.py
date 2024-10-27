from datetime import date, datetime, timedelta, timezone

from app.base.tests.views.base import BaseViewTest
from app.calendar.tests.factories import CalendarEventFactory


class BookingSlotsFactoryTest(BaseViewTest):
    day: str
    tz: str
    step_minutes: int

    _base_path = '/bookings/slots/trial/'

    @property
    def path(self):
        return (
            f"{self._base_path}?day={self.day}&timezone={self.tz}&"
            f"step_minutes={self.step_minutes}"
        )

    def test_create_slots_for_day(self):
        # Arrange
        day = date(2023, 6, 19)
        tz = timezone(timedelta(hours=3))  # UTC+3
        self.day = day.strftime('%Y-%m-%d')
        self.tz = '%2B00%3A00'
        self.step_minutes = 30
        CalendarEventFactory(
            start_time=datetime(2023, 6, 18, 23),  # 02:00 (UTC+3)
            end_time=datetime(2023, 6, 19),  # 3:00 (UTC+3)
            host=self.me,
        )
        CalendarEventFactory(
            start_time=datetime(2023, 6, 19, 8),  # 11:00 (UTC+3)
            end_time=datetime(2023, 6, 19, 9),  # 12:00 (UTC+3)
            guests=[self.me],
        )
        expected_busy_slots = [
            {
                'start_time': datetime(2023, 6, 19, 2, tzinfo=tz),
                'end_time': datetime(2023, 6, 19, 2, 30, tzinfo=tz),
            },
            {
                'start_time': datetime(2023, 6, 19, 2, 30, tzinfo=tz),
                'end_time': datetime(2023, 6, 19, 3, tzinfo=tz),
            },
            {
                'start_time': datetime(2023, 6, 19, 11, tzinfo=tz),
                'end_time': datetime(2023, 6, 19, 11, 30, tzinfo=tz),
            },
            {
                'start_time': datetime(2023, 6, 19, 11, 30, tzinfo=tz),
                'end_time': datetime(2023, 6, 19, 12, tzinfo=tz),
            },
        ]

        # Act
        response = self._test('get', {'slots': [...]})
        slots = response.json()['slots']

        # Assert
        for expected_slot in expected_busy_slots:
            self.assert_true(
                any(
                    slot['start_time'] == expected_slot['start_time']
                    and slot['end_time'] == expected_slot['end_time']
                    and not slot['is_free']
                    for slot in slots
                ),
                msg=f"Slot {expected_slot} is not busy as expected",
            )

        for slot in slots:
            if not any(
                slot['start_time'] == expected_slot['start_time']
                and slot['end_time'] == expected_slot['end_time']
                for expected_slot in expected_busy_slots
            ):
                self.assert_true(
                    slot['is_free'],
                    msg=f"Slot {slot} is expected to be free but it is not",
                )
