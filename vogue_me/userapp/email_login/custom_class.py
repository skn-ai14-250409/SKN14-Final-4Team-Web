from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


class CustomLoginViewForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=256)

    def clean(self):
        super().clean()

        email  = self.cleaned_data.get('username')
        passwd = self.cleaned_data.get('password')

        if email and passwd:
            user = authenticate(self.request, username=email, password=passwd)

            if not user.member.is_authed():
                raise forms.ValidationError("가입하신 이메일에서 본인인증 메일 확인 후 다시 시도해주세요.")

            self.user_cache = user
        else:
            raise forms.ValidationError("이메일과 비밀번호를 확인해주세요.")

        return self.cleaned_data


class CustomLoginView(LoginView):
    authentication_form = CustomLoginViewForm
    template_name = "app/userapp/login.html"
    extra_context={
        "GOOGLE_CLIENT_ID"  : settings.GOOGLE_CLIENT_ID,
        "KAKAO_CLIENT_ID"   : settings.KAKAO_CLIENT_ID,
        "NAVER_CLIENT_ID"   : settings.NAVER_CLIENT_ID,
    }