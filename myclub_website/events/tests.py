import datetime as dt

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event


class BuyTicketTestCase(TestCase):
    def setUp(self) -> None:
        Event.objects.create(
            name="Test event",
            event_date=timezone.now() + dt.timedelta(days=7),
            manager="Someone",
            description="Great event",
            tickets=3,
        )
        return super().setUp()

    def test_can_buy_tickets_when_available(self):
        event = Event.objects.filter(name="Test event").first()
        url = reverse('event_details', kwargs={'pk': event.pk})
        self.client.post(url, {
            'first_name': 'John',
            'last_name': 'Lennon',
            'email': 'jlennon@beatles.org',
            'tickets': 1,
        })

        response = self.client.get(url)
        self.assertContains(response, b'Available Tickets: 2')

    def test_can_buy_tickets_when_available_alt(self):
        # Arrange
        event = Event.objects.filter(name="Test event").first()
        url = reverse('event_details', kwargs={'pk': event.pk})
        
        # Act
        response = self.client.post(url, {
            'first_name': 'John',
            'last_name': 'Lennon',
            'email': 'jlennon@beatles.org',
            'tickets': 1,
        })

        event.refresh_from_db()
        attendee = event.attendees.first()

        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertEqual(event.tickets, 2)
        self.assertEqual(attendee.first_name, "John")
