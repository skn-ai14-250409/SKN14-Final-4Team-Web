# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from apiapp.models import ChatHistory
from mainapp.models.like import Like
from mainapp.models.search_history import SearchHistory
from mainapp.models.search_history_product import SearchHistoryProduct

from mainapp.models.influencer import Influencer


@login_required
def index(request):
    context = {}
    # 기존에 입력한 선호 스타일이 있는지 체크
    if ChatHistory.objects.filter(user_id=request.user.id).count() == 0:
        context["newbie"] = True

    # 마지막에 대화했던 AI 정보 호출해서 화면에 구성.
    last_id = ChatHistory.objects.select_related("influencer").last()
    try:
        last_ai = last_id.influencer.id
    except:
        last_ai = Influencer.objects.get(id=1)
    request.session["last_ai_id"] = last_ai.id
    context["last_ai"] = {
        "name"  : last_ai.name,
        "image" : last_ai.profile_img_url,
        "voice" : last_ai.voice_info,
    }

    return render(request, "app/mainapp/index.html", context)

def main(request):
    return render(request, "app/mainapp/main.html")

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
        impacts = [json.loads(item.product.impact) for item in items]
        water_saved = 0
        co2_saved   = 0
        for impact in impacts:
            water_saved += impact["water_saved_l"]
            co2_saved   += impact["co2_saved_kg"]
        context["water_saved"] = water_saved
        context["co2_saved"]   = co2_saved
    except:
        pass

    return render(request, "app/mainapp/detail.html", context)

def survey(request):
    return render(request, "app/mainapp/survey.html")

def chat(request):
    return render(request, "app/mainapp/chat.html")

def profile(request):
    return render(request, "app/mainapp/profile.html")

