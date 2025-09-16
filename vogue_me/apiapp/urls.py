from django.urls import path

from . import views as v

app_name = 'apiapp'

urlpatterns = [
    path('ask', v.ask_api , name="ask_api"),
    path('like/<int:search_id>', v.like_api , name="like_api"),

    path('set/last_ai/<int:ai_id>', v.set_last_ai , name="set_last_ai_api"),
]