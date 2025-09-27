from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Office, Visittime
from patient.models import Patient
from review.models import Review

User = get_user_model()

class ReviewTestCase(TestCase):
    def setUp(self):
        self.doc_user = User.objects.create_user(username="doc", password="123")
        self.doc = Doctor.objects.create(user=self.doc_user, field="Cardiology", np="555")
        self.office = Office.objects.create(
            doctor=self.doc, location="Tehran", phone_num="09123456789", price=100
        )

        self.patient_user = User.objects.create_user(username="patient", password="123")
        self.patient = Patient.objects.create(
            user=self.patient_user, na_id="1234567890", birth_date="2000-01-01"
        )

        self.visit = Visittime.objects.create(
            doctor=self.doc,
            office=self.office,
            patient=self.patient_user,
            duration_start=timezone.now() + timezone.timedelta(hours=1),
            duration_end=timezone.now() + timezone.timedelta(hours=2),
            booked_at=timezone.now()
        )

    def test_add_comment_success(self):
        self.client.login(username="patient", password="123")
        url = reverse("add_comment", args=[self.doc.id])
        data = {
            "comment_text": "Great doctor!",
            "rating": 5,
            "visit_time_id": self.visit.id
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("doctor_detail", args=[self.doc.id]))
        review = Review.objects.get(visit_time=self.visit)
        self.assertEqual(review.comment, "Great doctor!")
        self.assertEqual(review.rating, 5)

    def test_add_comment_without_visit(self):
        self.client.login(username="patient", password="123")
        url = reverse("add_comment", args=[self.doc.id])
        data = {"comment_text": "Nice", "rating": 4}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("doctor_detail", args=[self.doc.id]))
        self.assertEqual(Review.objects.count(), 0)

    def test_add_comment_twice_same_visit(self):
        self.client.login(username="patient", password="123")
        Review.objects.create(
            doctor=self.doc,
            patient=self.patient,
            comment="First comment",
            rating=5,
            visit_time=self.visit
        )
        url = reverse("add_comment", args=[self.doc.id])
        data = {
            "comment_text": "Second comment",
            "rating": 4,
            "visit_time_id": self.visit.id
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("doctor_detail", args=[self.doc.id]))
        self.assertEqual(Review.objects.count(), 1)

    def test_non_patient_cannot_add_comment(self):
        non_patient_user = User.objects.create_user(username="nonpatient", password="123")
        self.client.login(username="nonpatient", password="123")
        url = reverse("add_comment", args=[self.doc.id])
        data = {"comment_text": "Test", "rating": 3, "visit_time_id": self.visit.id}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("doctor_detail", args=[self.doc.id]))
        self.assertEqual(Review.objects.count(), 0)
