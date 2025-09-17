from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from mainapp.models.influencer import Influencer

GENDER_CATEGORIES = [
    ('M', '남성'),
    ('F', '여성'),
    ('E', '기타'),
]

class Member(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="member")
    height    = models.FloatField(null=False, default=0)
    birthday  = models.DateField(null=False, default=timezone.now)
    authed    = models.CharField(max_length=1, choices=[("Y","인증됨"),("N","미인증")], default="N")
    sns_type  = models.CharField(max_length=10)
    nickname  = models.CharField(max_length=100, null=True, default="default")
    gender    = models.CharField(max_length=10, null=True, choices=GENDER_CATEGORIES)
    prefer_material = models.CharField(max_length=100, null=True)
    prefer    = models.CharField(max_length=100, null=True)
    photo_url = models.CharField(max_length=256, null=False, default="/static/default_user.jpg")

    last_ai   = models.ForeignKey(Influencer, on_delete=models.SET_NULL, null=True, default=1)

    @classmethod
    def add_new_user(cls, email, first_name, last_name):
        return User.objects.create(username=email, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def add_new_member(cls, user, sns_type, height=0, birthday=timezone.now(), photo_url="/static/default_user.jpg"):
        return Member.objects.create(user=user, sns_type=sns_type, photo_url=photo_url, height=height, birthday=birthday)

    def is_authed(self):
        return "Y" == self.authed

    @property
    def age(self):
        if self.birthday:
            today = date.today()
            age = today.year - self.birthday.year
            age -= ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            return age
        return None





# Create your models here.
class RegisterUserForm(UserCreationForm):
    email    = forms.EmailField(required=True)     # User 의 email 속성을 덮어쓰기 위해 선언
    height   = forms.FloatField(required=False, label="키", min_value=0)
    birthday = forms.DateField(required=False, label="생일")
    gender   = forms.CharField(required=False, max_length=10, label="성별")
    prefer   = forms.CharField(required=False, max_length=100, label="선호 스타일")

    class Meta:
        model  = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if email:
            cleaned_data["username"] = email  # username 필드에 email 을 설정
        return cleaned_data

    def save(self):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]  # email → username
        user.email = self.cleaned_data["email"]
        user.save()
        return user



class NewbieSurveyForm(forms.ModelForm):
    birthday        = forms.DateTimeField(required=False)
    nickname        = forms.CharField(required=False, max_length=100)
    gender          = forms.CharField(required=False, max_length=10)
    prefer_material = forms.CharField(required=False, max_length=100)
    prefer          = forms.CharField(required=False, max_length=100)

    class Meta:
        model  = Member
        fields = ["gender", "birthday", "prefer", "prefer_material", "nickname"]
