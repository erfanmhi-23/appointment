from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Office, Visittime, Timesheet
from django.utils import timezone

User = get_user_model()

class PatientTest(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user("patient1", password="123")
        self.doc_user = User.objects.create_user("doc1", password="123")
        self.doc = Doctor.objects.create(user=self.doc_user, field="Cardiology", np="111")
        self.office = Office.objects.create(doctor=self.doc, location="Tehran", phone_num="09123456789", price=100)
        self.sheet = Timesheet.objects.create(
            office=self.office,
            start=timezone.now(),
            end=timezone.now() + timezone.timedelta(hours=1),
            duration=60
        )
        self.visit = Visittime.objects.create(
            doctor=self.doc,
            office=self.office,
            duration_start=timezone.now() + timezone.timedelta(hours=2),
            duration_end=timezone.now() + timezone.timedelta(hours=3)
        )

    def test_sign_up(self):
        url = reverse("sign_up")
        resp = self.client.get(url)
        assert resp.status_code == 200

        data = {"username":"newp", "password1":"12345678", "password2":"12345678"}
        resp = self.client.post(url, data)
        assert resp.status_code == 302
        assert User.objects.filter(username="newp").exists()

    def test_show_nobat(self):
        url = reverse("show_nobat", args=[self.doc.id])
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert resp.context["doctor"] == self.doc

    def test_reserve_visit(self):
        self.client.login(username="patient1", password="123")
        url = reverse("reserve_visit_time", args=[self.visit.id])
        self.client.post(url)
        self.visit.refresh_from_db()
        assert self.visit.patient == self.patient
        assert self.visit.booked_at is not None

    def test_cancel_visit(self):
        self.visit.patient = self.patient
        self.visit.save()
        self.client.login(username="patient1", password="123")
        url = reverse("cancel_visit_time", args=[self.visit.id])
        self.client.post(url)
        self.visit.refresh_from_db()
        assert self.visit.canceled_at is not None
