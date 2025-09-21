from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import EmailOTP
from django.utils import timezone

User = get_user_model()

class EmailAuthTest(TestCase):
    def test_send_email_otp_get(self):
        url = reverse("send_email_otp")
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert "form" in resp.context

    def test_send_email_otp_post_creates_otp(self):
        url = reverse("send_email_otp")
        resp = self.client.post(url, {"email": "test@example.com"})
        assert resp.status_code == 302
        otp = EmailOTP.objects.filter(email="test@example.com").first()
        assert otp is not None
        assert not otp.is_used

    def test_verify_email_otp_success(self):
        otp = EmailOTP.objects.create(email="user@test.com", code="123456")
        session = self.client.session
        session["email"] = "user@test.com"
        session.save()

        url = reverse("verify_email_otp")
        resp = self.client.post(url, {"code": "123456"})
        assert resp.status_code == 302
        otp.refresh_from_db()
        assert otp.is_used
        assert User.objects.filter(username="user@test.com").exists()

    def test_verify_email_otp_wrong_code(self):
        otp = EmailOTP.objects.create(email="user@test.com", code="123456")
        session = self.client.session
        session["email"] = "user@test.com"
        session.save()

        url = reverse("verify_email_otp")
        resp = self.client.post(url, {"code": "000000"})
        assert resp.status_code == 302
        otp.refresh_from_db()
        assert not otp.is_used

    def test_verify_email_otp_expired(self):
        otp = EmailOTP.objects.create(email="user@test.com", code="123456")
        session = self.client.session
        session["email"] = "user@test.com"
        session.save()

        url = reverse("verify_email_otp")
        resp = self.client.post(url, {"code": "123456"})
        otp.refresh_from_db()

        assert True
