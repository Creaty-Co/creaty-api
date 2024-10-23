from datetime import date, datetime, timedelta, timezone

from app.base.tests.base import BaseTest
from app.bookings.services.factories.slots import BookingSlotsFactory
from app.calendar.tests.factories import CalendarEventFactory
from app.users.tests.factories import UserFactory


class BookingSlotsFactoryTest(BaseTest):
    def test_create_slots_for_day(self):
        # Arrange
        user = UserFactory()
        factory = BookingSlotsFactory()
        tz = timezone(timedelta(hours=3))  # UTC+3
        day = date(2023, 6, 19)
        step_minutes = 30
        CalendarEventFactory(
            start_time=datetime(2023, 6, 18, 23),  # 02:00 (UTC+3)
            end_time=datetime(2023, 6, 19),  # 3:00 (UTC+3)
            host=user,
        )
        CalendarEventFactory(
            start_time=datetime(2023, 6, 19, 8),  # 11:00 (UTC+3)
            end_time=datetime(2023, 6, 19, 9),  # 12:00 (UTC+3)
            guests=[user],
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
        slots = factory.create_slots_for_day(
            user=user,
            day=day,
            tz=tz,
            step_minutes=step_minutes,
        )

        # Assert
        for expected_slot in expected_busy_slots:
            self.assert_true(
                any(
                    slot.start_time == expected_slot['start_time']
                    and slot.end_time == expected_slot['end_time']
                    and not slot.is_free
                    for slot in slots
                ),
                msg=f"Slot {expected_slot} is not busy as expected",
            )

        for slot in slots:
            if not any(
                slot.start_time == expected_slot['start_time']
                and slot.end_time == expected_slot['end_time']
                for expected_slot in expected_busy_slots
            ):
                self.assert_true(
                    slot.is_free,
                    msg=f"Slot {slot} is expected to be free but it is not",
                )
