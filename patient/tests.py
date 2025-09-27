from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from patient.models import Patient

User = get_user_model()


class PatientSignUpTests(TestCase):
    def test_get_sign_up_page(self):
        """فرم ثبت نام به درستی در GET نمایش داده می‌شود"""
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_post_valid_data_creates_patient(self):
        """ارسال داده معتبر باعث ایجاد User و Patient می‌شود"""
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'na_id': '1234567890',
            'birth_date': '1990-01-01',
        }
        response = self.client.post(reverse('sign_up'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(hasattr(user, 'patient_profile'))
        patient = user.patient_profile
        self.assertEqual(patient.na_id, '1234567890')

    def test_post_duplicate_username(self):
        """ثبت نام با نام کاربری تکراری خطا می‌دهد"""
        User.objects.create_user(username='testuser', password='12345')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'na_id': '1234567890',
            'birth_date': '1990-01-01',
        }
        response = self.client.post(reverse('sign_up'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "این نام کاربری قبلاً ثبت شده است.")
