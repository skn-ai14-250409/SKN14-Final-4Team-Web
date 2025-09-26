# Create your views here.
import json

from apiapp.models import ChatHistory
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from mainapp.models.influencer import Influencer
from mainapp.models.like import Like
from mainapp.models.search_history import SearchHistory
from mainapp.models.search_history_product import SearchHistoryProduct
from userapp.models import NewbieSurveyForm


def __get_my_last_ai_info(ai_id):
    last_ai = Influencer.objects.get(id=ai_id)
    return {
        "id"   : last_ai.id,
        "name" : last_ai.name,
        "image": last_ai.profile_img_url,
        "voice": last_ai.voice_info,
    }

def robots_txt(request):
    content = "User-agent: *\nDisallow: /\n"
    return HttpResponse(content, content_type="text/plain")

@login_required
def index(request):
    if not ChatHistory.objects.filter(user_id=request.user.id).exists():
        return redirect("mainapp:chat")

    # 마지막에 대화했던 AI 정보 호출해서 화면에 구성.
    return redirect("mainapp:chat")

def detail(request, id):
    if not SearchHistory.objects.filter(id=id).exists():
        return HttpResponse(status=404)

    look  = SearchHistory.objects.get(id=id)
    items = SearchHistoryProduct.objects.filter(search_id=id)
    like  = Like.objects.filter(search_id=id, user=request.user).exists()
    context = {
        "look" : look,
        "products" : [item.product for item in items],
        "like" : like
    }
    try:
        water_saved = 0
        co2_saved   = 0
        for item in items:
            water = json.loads(item.product.water_saved_l)
            co2   = json.loads(item.product.co2_saved_kg)

            water_saved += water.get("water_saved_l", 0)
            co2_saved += co2.get("co2_saved_kg", 0)
        context["water_saved_l"] = round(water_saved, 2)
        context["co2_saved_kg"]  = round(co2_saved, 2)
    except:
        pass

    return render(request, "app/mainapp/detail.html", context)

def survey(request):
    if request.method == "POST":
        result = {"status" : False}
        data   = json.loads(request.body)
        form   = NewbieSurveyForm(data, instance=request.user.member)
        if form.is_valid():
            nickname = data.get('nickname') or form.cleaned_data.get('nickname')
            request.user.first_name = nickname
            request.user.save()

            member = form.save(commit=False)
            member.survey_completed = True
            member.save()
            result["status"] = True
        return JsonResponse(result)
    else:
        if request.user.member.survey_completed:
            return redirect("mainapp:profile")

        last_ai = __get_my_last_ai_info(request.user.member.last_ai_id)
        return render(request, "app/mainapp/survey.html", last_ai)

@login_required
def chat(request):
    ai_id     = request.user.member.last_ai_id
    ai_id     = request.GET.get("influencer", ai_id)
    request.session["last_ai_id"] = ai_id

    last_ai   = __get_my_last_ai_info(ai_id)
    chat_log  = ChatHistory.objects.filter(user_id=request.user.id, influencer_id=ai_id).all()[:20]
    chat_log  = sorted(chat_log, key=lambda x:x.talked_at, reverse=False)

    voice_enabled = request.user.member.voice_enabled

    context = {
        "last_ai"  : last_ai,
        "all_ai"   : Influencer.objects.all(),
        "chat_log" : chat_log,
        "voice_enabled" : voice_enabled,
        "ai_id"    : ai_id,
    }
    return render(request, "app/mainapp/chat.html", context)

def toggle_voice(request):
    data = json.loads(request.body)
    enabled = data.get('voice_enabled', True)
    profile = request.user.member
    profile.voice_enabled = enabled
    profile.save()
    return JsonResponse({'success': True, 'voice_enabled': profile.voice_enabled})

def profile(request):
    return render(request, "app/mainapp/profile.html")

def save_profile(request):
    if request.method == "POST":
        try:
            data   = json.loads(request.body.decode("utf-8"))
            user   = request.user
            member = user.member

            member.nickname        = data.get("nickname", member.nickname)
            member.prefer          = data.get("prefer", member.prefer)
            member.prefer_material = data.get("prefer_material", member.prefer_material)
            member.save()

            return JsonResponse({"success": True, "message": "프로필 저장 완료"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "잘못된 요청"}, status=405)

def chat_history(request):
    user_id = request.user.id

    latest_talk = (
        ChatHistory.objects
        .filter(user_id=user_id, influencer=OuterRef("influencer"))
        .order_by("-talked_at")
    )

    qs = (
        ChatHistory.objects
        .filter(user_id=user_id)
        .annotate(
            latest_talked_at=Subquery(latest_talk.values("talked_at")[:1])
        )
        .filter(talked_at=F("latest_talked_at"))
    )
    chat_rooms = [
        {
            "ai_id"    : chat_log.influencer.id,
            "ai_name"  : chat_log.influencer.name,
            "ai_image" : chat_log.influencer.profile_img_url,
            "chat_time": chat_log.log_time,
            "chat_text": chat_log.text_only
        }
        for chat_log in qs
    ]

    return render(request, "app/mainapp/chat_history.html", {"chat_rooms" : chat_rooms})

@login_required
def delete_chats(request):
    data = json.loads(request.body.decode('utf-8'))
    chat_ids = data.get("chat_ids", [])

    if not chat_ids:
        return JsonResponse({"success": False, "message": "삭제할 항목이 없습니다."})
        
    ChatHistory.objects.filter(influencer_id__in=chat_ids, user=request.user).delete()

    return JsonResponse({"success": True})

def likes(request):
    likes  = Like.objects.prefetch_related("search").filter(user=request.user)
    styles = [like.search for like in likes]
    return render(request, "app/mainapp/likes.html", {"liked_styles" : styles})


