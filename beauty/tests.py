from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Appointment, Institute, Service


class AppointmentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username='institut', password='motdepasse123', role=User.Role.INSTITUTE)
        cls.client_user = User.objects.create_user(username='cliente', password='motdepasse123')
        cls.institute = Institute.objects.create(
            owner=cls.owner, name='Belle Peau', slug='belle-peau', description='Soins',
            neighborhood='Koulouba', address='Rue des arts', phone='70000000',
        )
        cls.service = Service.objects.create(institute=cls.institute, name='Soin visage', price=8000)

    def test_booking_requires_authentication(self):
        response = self.client.get(reverse('book', args=[self.institute.slug]))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('book', args=[self.institute.slug])}")

    def test_authenticated_client_can_book_an_institute_service(self):
        self.client.force_login(self.client_user)

        response = self.client.post(reverse('book', args=[self.institute.slug]), {
            'service': self.service.id, 'starts_at': '2026-09-20T14:30', 'note': 'Peau sensible',
        })

        self.assertRedirects(response, reverse('institutes'))
        appointment = Appointment.objects.get()
        self.assertEqual(appointment.client, self.client_user)
        self.assertEqual(appointment.service, self.service)
        self.assertEqual(appointment.note, 'Peau sensible')
