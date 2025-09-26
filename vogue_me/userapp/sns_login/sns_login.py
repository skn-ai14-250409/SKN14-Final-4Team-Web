import requests
from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import render, redirect

from mailapp.models import *
from userapp.models import Member


class SnsLogin:
    def __init__(self, provider, cid, secret):
        self.provider = provider
        self.cid      = cid
        self.secret   = secret

    def get_auth_params(self, request):
        return {
            "code"          : request.GET.get("code"),
            "client_id"     : self.cid,
            "client_secret" : self.secret,
            "redirect_uri"  : f"http://{request.get_host()}/user/sns_login/{self.provider}",
            "grant_type"    : "authorization_code",
        }

    def get_access_token(self, token_url, params):
        headers = {"Content-Type" : "application/x-www-form-urlencoded"}
        data    = self.get_json_response(token_url, params, headers)
        token   = data.get('access_token')
        return token

    def get_json_response(self, url, params=None, headers=None):
        # response = requests.get(url, params, headers=headers)
        response = requests.post(url, data=params, headers=headers, timeout=300)
        response.raise_for_status()
        return response.json()

    def run_when_user_exist(self, request, email:str):
        login_user = User.objects.get(username=email)
        sns_type   = login_user.member.sns_type
        if sns_type != self.provider:
            return render(request, "layout/redirect.html", {"redirect":reverse("userapp:login"), "msg":"로그인하실 계정종류를 확인해주세요."})

        # is_authed  = login_user.auth.order_by("-created_at").first().is_authed()
        is_authed  = login_user.member.is_authed()
        if is_authed:
            login(request, login_user)
            return redirect("mainapp:index")
        else:
            return render(request, "layout/redirect.html", {"redirect":reverse("userapp:login"), "msg":"가입하신 메일에서 본인인증을 완료해주세요."})

    def run_when_user_not_exist(self, request, email:str, first_name, last_name, photo_url):
        new_user   = Member.add_new_user(email, first_name, last_name)
        new_member = Member.add_new_member(new_user, self.provider, photo_url=photo_url)
        LoginAuth.send_auth_mail(request, new_user)
        return render(request, "layout/redirect.html", {"redirect":reverse("userapp:login"), "msg":"가입하신 이메일로 본인인증을 위한 메일이 발송되었습니다."})

    @transaction.atomic
    def login(self, request):
        pass