from django.urls import path

from . import views as v

app_name = 'mainapp'

urlpatterns = [
    path(''                 , v.index , name="index"),
    path('detail/<int:id>'  , v.detail, name="detail"),

    #########
    path('survey', v.survey, name="survey"),
    path('profile', v.profile, name="profile"),
    path('chat' , v.chat , name="chat"),
    path('toggle-voice/', v.toggle_voice, name="toggle_voice"),
    path("user/profile/save", v.save_profile, name="save_profile"),
    path('chat_history', v.chat_history, name="chat_history"),
    path("chat/delete/", v.delete_chats, name="delete_chats"),
    path('likes', v.likes, name="likes"),
]