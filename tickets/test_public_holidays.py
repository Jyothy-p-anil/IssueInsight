
from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase

from django.urls import reverse


from tickets.services.public_holidays import (
    get_kerala_public_holidays,
)


class PublicHolidayServiceTests(TestCase):

    def setUp(self):
        cache.clear()

    @patch("tickets.services.public_holidays.urlopen")
    def test_successful_api_response(self, mock_urlopen):
        from io import BytesIO

        response_data = (
            b'{"data": ['
            b'{"date": "2026-01-26", '
            b'"name": "Republic Day", "level": "state"},'
            b'{"date": "2026-08-26", '
            b'"name": "Thiruvonam", "level": "state"}'
            b']}'
        )

        mock_urlopen.return_value.__enter__.return_value = (
            BytesIO(response_data)
        )

        holidays = get_kerala_public_holidays(2026)

        self.assertEqual(len(holidays), 2)
        self.assertEqual(
            holidays[0]["name"], "Republic Day"
        )
        self.assertEqual(
            holidays[1]["name"], "Thiruvonam"
        )

    @patch("tickets.services.public_holidays.urlopen")
    def test_api_failure_returns_empty_list(self, mock_urlopen):
        mock_urlopen.side_effect = TimeoutError()

        holidays = get_kerala_public_holidays(2026)

        self.assertEqual(holidays, [])

    @patch("tickets.services.public_holidays.urlopen")
    def test_api_failure_is_not_cached(self, mock_urlopen):
        mock_urlopen.side_effect = TimeoutError()

        get_kerala_public_holidays(2026)

        self.assertIsNone(
            cache.get("kerala_public_holidays_2026")
        )

    @patch("tickets.services.public_holidays.urlopen")
    def test_cached_holidays_avoid_api_request(self, mock_urlopen):
        cached_holidays = [
            {
                "date": "2026-01-26",
                "name": "Republic Day",
            }
        ]

        cache.set(
            "kerala_public_holidays_2026",
            cached_holidays,
            86400,
        )

        holidays = get_kerala_public_holidays(2026)

        self.assertEqual(holidays, cached_holidays)
        mock_urlopen.assert_not_called()

    @patch("tickets.services.public_holidays.urlopen")
    def test_only_state_holidays_are_included(self, mock_urlopen):
        from io import BytesIO

        response_data = (
            b'{"data": ['
            b'{"date": "2026-01-26", '
            b'"name": "Republic Day", "level": "state"},'
            b'{"date": "2026-01-03", '
            b'"name": "Central Holiday", "level": "central"}'
            b']}'
        )

        mock_urlopen.return_value.__enter__.return_value = (
            BytesIO(response_data)
        )

        holidays = get_kerala_public_holidays(2026)

        self.assertEqual(len(holidays), 1)
        self.assertEqual(
            holidays[0]["name"], "Republic Day"
        )

class PublicHolidayCalendarTests(TestCase):

    @patch("tickets.views.get_kerala_public_holidays")
    def test_calendar_contains_twelve_months(self, mock_holidays):
        mock_holidays.return_value = []

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["calendar_data"]),
            12,
        )

    @patch("tickets.views.get_kerala_public_holidays")
    def test_holiday_is_attached_to_correct_date(self, mock_holidays):
        mock_holidays.return_value = [
            {
                "date": "2026-08-26",
                "name": "Thiruvonam",
            }
        ]

        with patch("tickets.views.timezone.localdate") as mock_today:
            from datetime import date
            mock_today.return_value = date(2026, 8, 20)

            response = self.client.get(reverse("home"))

        august = response.context["calendar_data"][7]

        matching_days = [
            day
            for week in august["weeks"]
            for day in week
            if day["date"] == "2026-08-26"
        ]

        self.assertEqual(len(matching_days), 1)
        self.assertEqual(
            matching_days[0]["holidays"],
            ["Thiruvonam"],
        )

    @patch("tickets.views.get_kerala_public_holidays")
    def test_multiple_holidays_on_same_date(self, mock_holidays):
        mock_holidays.return_value = [
            {
                "date": "2026-08-28",
                "name": "Fourth Onam",
            },
            {
                "date": "2026-08-28",
                "name": "Avani Avittom",
            },
        ]

        with patch("tickets.views.timezone.localdate") as mock_today:
            from datetime import date
            mock_today.return_value = date(2026, 8, 20)

            response = self.client.get(reverse("home"))

        august = response.context["calendar_data"][7]

        matching_day = next(
            day
            for week in august["weeks"]
            for day in week
            if day["date"] == "2026-08-28"
        )

        self.assertEqual(
            matching_day["holidays"],
            ["Fourth Onam", "Avani Avittom"],
        )

    @patch("tickets.views.get_kerala_public_holidays")
    def test_calendar_displays_holiday_information(self, mock_holidays):
        mock_holidays.return_value = [
            {
                "date": "2026-08-26",
                "name": "Thiruvonam",
            }
        ]

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Thiruvonam")
        self.assertContains(response, "2026-08-26")

    @patch("tickets.views.get_kerala_public_holidays")
    def test_home_remains_accessible_when_api_fails(self, mock_holidays):
        mock_holidays.return_value = []

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Public holiday information is currently unavailable.",
        )
