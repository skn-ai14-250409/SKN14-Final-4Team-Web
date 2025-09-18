import json
import os

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

from apiapp.models import ChatHistory
from mainapp.models.like import Like


@login_required
def ask_api(request):
    raw_data  = request.body.decode('utf-8')
    json_data = json.loads(raw_data)

    msg     = json_data['query']
    user_id = request.user.id
    ai_id   = request.session.get('last_ai_id', 1)
    _save_chat(user_id, msg, ai_id)

    result, data = _get_result(msg, user_id, ai_id)
    print(f"{data=}")
    _save_chat(user_id, data, ai_id, "ai")

    return result

def _save_chat(user_id, style_text, ai_id=1, talker_type="user", optional_text=None, voice_url=None):
    return ChatHistory.objects.create(
        user_id         = user_id,
        influencer_id   = ai_id,
        style_text      = style_text,
        talker_type     = talker_type,
        optional_text   = optional_text,
        voice_url       = voice_url
    )

def _get_result(msg:str, user_id, ai_id):
    # # 가라 데이터 반환
    # import os
    # from django.conf import settings
    # dummy_json = os.path.join(settings.BASE_DIR, "static/dummy", 'dummy_result.json')
    # with open(dummy_json, "r", encoding="utf-8") as f:
    #     return json.load(f)
    try:
        url = "https://api.looplabel.site/api/ask"
        params = {"query": msg, "user_id": user_id, "ai_id": ai_id}
        headers = {"Content-Type": "application/json"}
        # response = requests.post(url, data=params, headers=headers)
        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()

        result_type = response.headers.get('Content-Type', '')
        if "application/json" in result_type:   return JsonResponse(response.json()), response.json()
        else:                                   return HttpResponse(response.text), response.text
    except Exception as e:
        print(e)
        __msg = "죄송합니다. 문제가 생긴거 같네요."
        return HttpResponse(__msg), __msg

@login_required
def like_api(request, search_id):
    user_id = request.user.id
    like = Like.objects.filter(search_id=search_id, user_id=user_id)
    if like.exists():
        like.delete()
        result = { "like" : False }
    else:
        Like.objects.create(search_id=search_id, user_id=user_id)
        result = { "like" : True }

    return JsonResponse(result)

@login_required
def like_check(request):
    user_id = request.user.id
    style_ids = request.GET.getlist("style_id")
    style_ids = list(set(style_ids))
    like_ids = Like.objects.filter(search_id__in=style_ids, user_id=user_id).values_list("search_id", flat=True)

    return JsonResponse({"like" : list(like_ids)})

@login_required
def set_last_ai(request, ai_id):
    member = request.user.member
    member.last_ai_id = ai_id
    member.save()

    request.session["last_ai_id"] = ai_id
    print(f"{request.session.get("last_ai_id")=}")

    return JsonResponse({"status": True})