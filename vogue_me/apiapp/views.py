import json
import os

import requests
from apiapp.models import ChatHistory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from mainapp.models.like import Like


@login_required
def ask_api(request):
    raw_data  = request.body.decode('utf-8')
    json_data = json.loads(raw_data)

    msg     = json_data['query']
    user_id = request.user.id
    ai_id   = request.session.get('last_ai_id', 1)
    _save_chat(user_id, msg, ai_id)

    try:
        result, data = _get_result(msg, user_id, ai_id)
        _save_chat(user_id, data, ai_id, "ai")
        return result
    except Exception as e:
        print(e)
        return HttpResponse("죄송합니다. 문제가 생긴거 같네요.")


def _save_chat(user_id, style_text, ai_id=1, talker_type="user", optional_text=None, voice_url=None):
    return ChatHistory.objects.create(
        user_id         = user_id,
        influencer_id   = ai_id,
        style_text      = style_text,
        talker_type     = talker_type,
        optional_text   = optional_text,
        voice_url       = voice_url
    )

ASK_API_URL = os.getenv("FAST_API_ASK", "https://api.looplabel.site/api/ask")
def _get_result(msg:str, user_id, ai_id):
    url     = ASK_API_URL
    params  = {"query": msg, "user_id": user_id, "ai_id": ai_id}
    headers = {"Content-Type": "application/json"}
    # response = requests.post(url, data=params, headers=headers)
    response = requests.post(url, json=params, headers=headers, timeout=(10, 600))
    response.raise_for_status()

    result_type = response.headers.get('Content-Type', '')
    if "application/json" in result_type:   return JsonResponse(response.json()), response.json()
    else:                                   return HttpResponse(response.text), response.text

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

    return JsonResponse({"status": True})