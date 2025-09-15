# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from apiapp.models import ChatHistory
from mainapp.models.like import Like
from mainapp.models.search_history import SearchHistory
from mainapp.models.search_history_product import SearchHistoryProduct
from mainapp.models.influencer import Influencer
from userapp.models import NewbieSurveyForm


def __get_my_last_ai_info(request):
    last_ai = Influencer.objects.get(id=request.user.member.last_ai_id)
    return {
        "id"   : last_ai.id,
        "name" : last_ai.name,
        "image": last_ai.profile_img_url,
        "voice": last_ai.voice_info,
    }

@login_required
def index(request):
    if not ChatHistory.objects.filter(user_id=request.user.id).exists():
        return redirect("mainapp:survey")

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
    if request.method == "POST":
        result = {"status" : False}
        data   = json.loads(request.body)
        form   = NewbieSurveyForm(data, instance=request.user.member)
        if form.is_valid():
            form.save()
            result["status"] = True
        print(form.errors)
        return JsonResponse(result)
    else:
        last_ai = __get_my_last_ai_info(request)
        return render(request, "app/mainapp/survey.html", last_ai)

def chat(request):
    return render(request, "app/mainapp/chat.html")

def profile(request):
    return render(request, "app/mainapp/profile.html")

def chat_history(request):
    return render(request, "app/mainapp/chat_history.html")