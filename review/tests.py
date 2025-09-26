from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Visittime
from patient.models import Patient
from review.models import Review

User = get_user_model()

class ReviewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_doc = User.objects.create_user(username="doc", password="123")
        cls.user_patient = User.objects.create_user(username="patient", password="123")
        
        cls.doc = Doctor.objects.create(user=cls.user_doc, field="Cardiology", np="111")
        cls.patient = Patient.objects.create(user=cls.user_patient)

        cls.visit = Visittime.objects.create(
            doctor=cls.doc,
            office=cls.doc.office_set.first() if cls.doc.office_set.exists() else None,
            duration_start=timezone.now(),
            duration_end=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_add_review_success(self):
        self.client.login(username="patient", password="123")
        url = reverse("add_comment", args=[self.doc.id])
        data = {
            "comment_text": "تست نظر",
            "rating": "5",
            "visit_time_id": self.visit.id
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Review.objects.filter(visit_time=self.visit).exists())

    def test_add_review_without_visit(self):
        self.client.login(username="patient", password="123")
        url = reverse("add_comment", args=[self.doc.id])
        data = {
            "comment_text": "تست بدون نوبت",
            "rating": "4",
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Review.objects.exists())

    def test_add_review_duplicate(self):
        Review.objects.create(
            doctor=self.doc,
            patient=self.patient,
            comment="قبلی",
            rating=5,
            visit_time=self.visit
        )
        self.client.login(username="patient", password="123")
        url = reverse("add_comment", args=[self.doc.id])
        data = {
            "comment_text": "نظر جدید",
            "rating": "4",
            "visit_time_id": self.visit.id
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Review.objects.filter(visit_time=self.visit).count(), 1)
