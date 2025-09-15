from django.urls import path

from . import views as v

app_name = 'mainapp'

urlpatterns = [
    path(''                 , v.index , name="index"),
    path('detail/<int:id>'  , v.detail, name="detail"),

    #########
    path('survey', v.survey, name="survey"),
    path('chat' , v.chat , name="chat"),
    path('profile', v.profile, name="profile"),
    path('chat_history', v.chat_history, name="chat_history"),
]