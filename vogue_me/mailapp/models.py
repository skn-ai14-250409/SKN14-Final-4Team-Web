import re
import secrets
from datetime import timedelta

from cryptography.fernet import Fernet
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .utils import send_mail_with, MailForm


class LoginAuth(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth')
    auth_code   = models.CharField(max_length=10)
    cipher_key  = models.CharField(max_length=44, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    expires_at  = models.DateTimeField()
    authed_at   = models.DateTimeField(null=True)

    @classmethod
    def send_auth_mail(cls, request, user):
        new_auth = LoginAuth.objects.create(
            user=user,
        )
        context = {
            "auth_link" : "http://"+request.META['HTTP_HOST'] + reverse('userapp:verify_auth_link', kwargs={"user_id":user.id, "encrypted_code" : new_auth.get_encrypted_code()}),
            "due_time" : new_auth.expires_at.strftime("%Y.%m.%d %H:%M:%S")
        }
        send_mail_with(user.email, "[LoopLabel] 본인확인 메일", MailForm.AUTH_LINK, context)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.auth_code is None or not self.auth_code:
            token = secrets.token_urlsafe(16)
            token = re.sub(r"[^a-zA-Z\d]", "", token)[:8].upper()
            self.auth_code = token

        # 키 생성 (안전하게 보관해야 함)
        if self.cipher_key is None or not self.cipher_key:
            self.cipher_key = Fernet.generate_key().decode("utf-8")

    def is_authed(self):
        return self.authed_at is not None

    def get_encrypted_code(self):
        f = Fernet(self.cipher_key.encode("utf-8"))

        # 데이터 암호화
        data_to_encrypt = f"{self.user.username}::{self.auth_code}".encode("utf-8")
        return f.encrypt(data_to_encrypt).decode("utf-8")

    def is_expired(self):
        return self.expires_at < timezone.now()

    def is_valid(self, encrypted_code):
        f = Fernet(self.cipher_key.encode("utf-8"))
        decrypted = f.decrypt(encrypted_code.encode("utf-8")).decode("utf-8")
        decrypted = decrypted.split("::")
        if self.user.email == decrypted[0] and self.auth_code == decrypted[1]:
            self.authed_at = timezone.now()
            self.save()
            self.user.member.authed = "Y"
            self.user.member.save()
            return True

        return False

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)