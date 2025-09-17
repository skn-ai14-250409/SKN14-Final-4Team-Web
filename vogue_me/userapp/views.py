import json

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from mailapp.models import *

from .models import NewbieSurveyForm
from .sns_login.google import Google
from .sns_login.kakao import Kakao
from .sns_login.naver import Naver

google = Google()
kakao  = Kakao()
naver  = Naver()



# 로그인할 지, 회원가입할 지 선택하는 화면
def signin_or_up(request):
    return render(request, "app/userapp/signin_or_up.html", {"GOOGLE_CLIENT_ID"  : settings.GOOGLE_CLIENT_ID})

# 회원가입 방법중에 구글로 할지 이메일 가입할 지 선택하는 화면
def signup_choice(request):
    return render(request, "app/userapp/signup_choice.html", {"GOOGLE_CLIENT_ID"  : settings.GOOGLE_CLIENT_ID})

# SNS 회원가입 또는 SNS 로그인
def sns_login(request, provider):
    if provider == "google":  return google.login(request)
    if provider == "kakao":   return kakao.login(request)
    if provider == "naver":   return naver.login(request)

    return HttpResponse("sns login done")

# 이메일로 회원가입
@transaction.atomic
def signup(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                form.add_error("email", "이미 가입된 계정입니다.")
            else:
                user = form.save()
                LoginAuth.send_auth_mail(request, user)
                # Member.add_new_member(user=user, sns_type="email", height=form.cleaned_data["height"], birthday=form.cleaned_data["birthday"])
                Member.add_new_member(user=user, sns_type="email")
                return render(request, "layout/redirect.html", {"redirect":reverse("userapp:login"), "msg":"가입하신 이메일로 본인인증을 위한 메일이 발송되었습니다."})
        form.add_error(None, '이 필드는 필수입니다.')
    else:
        form = RegisterUserForm()

    return render(request, "app/userapp/signup.html", {"form":form, "GOOGLE_CLIENT_ID"  : settings.GOOGLE_CLIENT_ID})

# 회원가입할 때 이메일이 중복인지 검사
def check_email_dup(request):
    if request.method == "GET": return redirect("mainapp:index")

    data = json.loads(request.body.decode('utf-8'))
    email = data.get("email")
    return JsonResponse({ "already_exist" : User.objects.filter(email=email).exists() })

# 본인인증 메일에서 버튼 클릭 시 인증 상태 확인.
def verify_auth_link(request, user_id, encrypted_code):
    if not User.objects.filter(id=user_id).exists():
        return render(request, "layout/redirect.html", {"redirect":":CLOSE", "msg":"본인인증 주소를 확인해주세요."})

    user = User.objects.get(id=user_id)
    auth = user.auth.order_by("-created_at").first()
    if not auth:
        return render(request, "layout/redirect.html", {"redirect":":CLOSE", "msg":"본인인증 주소를 확인해주세요."})

    if auth.is_authed():
        return render(request, "layout/redirect.html", {"redirect":":CLOSE", "msg":"인증이 완료된 링크입니다."})

    if auth.is_expired():
        LoginAuth.send_auth_mail(request, user)
        return render(request, "layout/redirect.html", {"redirect":":CLOSE", "msg":"인증기간이 만료되어, 신규 본인인증메일을 발송하였습니다.\\r\\n새로운 본인인증메일에서 다시 시도해주세요."})

    if auth.is_valid(encrypted_code):
        login(request, user)
        return render(request, "layout/redirect.html", {"redirect":reverse("mainapp:index"), "msg":"본인인증이 완료되었습니다."})
    else:
        return render(request, "layout/redirect.html", {"redirect":":CLOSE", "msg":"본인인증 주소를 확인해주세요."})



def _logout(request):
    try:
        auth.logout(request)
    except Exception as e:
        print(e)

def password_change_done(request):
    _logout(request)
    return render(request, "layout/redirect.html", {"redirect":reverse("mainapp:index"), "msg":"비밀번호 변경이 완료되었습니다.\\r\\n변경한 비밀번호로 다시 로그인해주세요."})

def logout(request):
    _logout(request)
    return redirect("userapp:signin_or_up")


@login_required
def profile_save(request):
    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')
        json_data = json.loads(raw_data)

        form = NewbieSurveyForm(json_data, instance=request.user.member)
        if form.is_valid():
            member = form.save()
            user = request.user
            user.member = member
            auth.login(request, user)
            messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

    return HttpResponse(status=400)

def mypage_profile(request):
    context = { 'main_active_tab': "mypage", "mypage_active_tab": "profile" }
    return render(request, 'app/mainapp/main.html', context)

@csrf_exempt
@require_POST
def toggle_like(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        # 실제로는 Like 모델과 상호작용
        return JsonResponse({'success': True, 'liked': True})
    except:
        return JsonResponse({'error': 'Invalid request'}, status=400)