from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Office, Timesheet, Visittime
from user.models import EmailOTP

User = get_user_model()

class DoctorViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.doc_user = User.objects.create_user(username="doc1", password="123")
        cls.doc = Doctor.objects.create(user=cls.doc_user, field="Cardiology", np="111")
        cls.office = Office.objects.create(
            doctor=cls.doc, location="Tehran", phone_num="09123456789", price=100
        )

    def test_list_and_detail(self):
        resp = self.client.get(reverse("doctor_list"))
        assert resp.status_code == 200
        assert self.doc in resp.context["page_obj"]

        resp = self.client.get(reverse("doctor_detail", args=[self.doc.id]))
        assert resp.status_code == 200
        assert resp.context["doctor"] == self.doc

        resp = self.client.get(reverse("doctor_detail", args=[999]))
        assert resp.status_code == 404

    def test_search(self):
        resp = self.client.get(reverse("doctor_search"), {"q": "Cardio"})
        assert resp.status_code == 200
        assert self.doc in resp.context["doctors"]

        resp = self.client.get(reverse("doctor_search"))
        assert resp.status_code == 200
        assert self.doc in resp.context["doctors"]

    def test_office_list(self):
        resp = self.client.get(reverse("office_list"))
        assert resp.status_code == 200
        assert self.office in resp.context["offices"]

        resp = self.client.get(reverse("office_list"), {"location": "Teh"})
        assert resp.status_code == 200
        assert self.office in resp.context["offices"]


class VisitTimeTest(TestCase):
    def setUp(self):
        self.doc_user = User.objects.create_user(username="doc", password="123")
        self.doc = Doctor.objects.create(user=self.doc_user, field="Cardiology", np="222")
        self.office = Office.objects.create(doctor=self.doc, location="Tehran", phone_num="09123456789", price=150)
        self.patient = User.objects.create_user(username="patient", password="123")
        self.visit = Visittime.objects.create(
            doctor=self.doc,
            office=self.office,
            duration_start=timezone.now() + timezone.timedelta(hours=1),
            duration_end=timezone.now() + timezone.timedelta(hours=2)
        )

    def test_reserve_visit(self):
        self.client.login(username="patient", password="123")
        url = reverse("reserve_visit_time", args=[self.visit.id])
        self.client.post(url)
        self.visit.refresh_from_db()
        assert self.visit.patient == self.patient
        assert self.visit.booked_at is not None

    def test_cancel_visit(self):
        self.visit.patient = self.patient
        self.visit.save()
        self.client.login(username="patient", password="123")
        url = reverse("cancel_visit_time", args=[self.visit.id])
        self.client.post(url)
        self.visit.refresh_from_db()
        assert self.visit.canceled_at is not None

    def test_free_times_list(self):
        url = reverse("doctor_free_times", args=[self.doc.id])
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert self.visit in resp.context["free_times"]


class AddDoctorTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", password="123")
        self.user = User.objects.create_user(username="newdoc", password="123")

    def test_add_doctor_access(self):
        url = reverse("add_doctor")
        resp = self.client.get(url)
        assert resp.status_code == 302

        self.client.login(username="newdoc", password="123")
        resp = self.client.get(url)
        assert resp.status_code == 403

        self.client.login(username="admin", password="123")
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert "form" in resp.context

    def test_add_doctor_post(self):
        self.client.login(username="admin", password="123")
        url = reverse("add_doctor")
        data = {"user": self.user.id, "field": "Dermatology", "np": "555"}
        resp = self.client.post(url, data)
        assert resp.status_code == 302
        assert Doctor.objects.filter(user=self.user).exists()


class TimesheetTest(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username="staff", password="123", is_staff=True)
        self.user = User.objects.create_user(username="doc", password="123")
        self.doc = Doctor.objects.create(user=self.user, field="Cardiology", np="333")
        self.office = Office.objects.create(doctor=self.doc, location="Tehran", phone_num="09123456789", price=200)
        self.sheet = Timesheet.objects.create(
            office=self.office, start=timezone.now(), end=timezone.now() + timezone.timedelta(hours=1), duration=60
        )

    def test_timesheet_access(self):
        resp = self.client.get(reverse("timesheet_list"))
        assert resp.status_code == 302

        self.client.login(username="staff", password="123")
        resp = self.client.get(reverse("timesheet_list"))
        assert resp.status_code == 200
        assert self.sheet in resp.context["timesheets"]


class HomeTest(TestCase):
    def test_home(self):
        resp = self.client.get(reverse("home"))
        assert resp.status_code == 200


class ModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="doc", password="123")
        self.doc = Doctor.objects.create(user=self.user, field="Cardiology", np="444")
        self.office = Office.objects.create(doctor=self.doc, location="Tehran", phone_num="09123456789", price=100)
        self.visit = Visittime.objects.create(
            doctor=self.doc, office=self.office,
            duration_start=timezone.now(), duration_end=timezone.now() + timezone.timedelta(hours=1)
        )

    def test_str_methods(self):
        assert str(self.doc) == f"Dr.{self.user.username} - Cardiology"
        assert str(self.office) == f"{self.doc} - Tehran"
        assert str(self.visit).startswith(str(self.doc))

    def test_email_otp(self):
        otp = EmailOTP.objects.create(email="a@gmail.com", code="123456")
        assert not otp.is_used
        assert not otp.is_expired()
        code = EmailOTP.generate_otp()
        assert len(code) == 6
        assert code.isdigit()

    def test_user_str(self):
        assert str(self.user) == self.user.username
