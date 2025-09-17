from django.contrib.auth import views as auth_views
from django.urls import path

from . import views as v
from .email_login.custom_class import CustomLoginView

app_name = 'userapp'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name="app/userapp/login.html"), name="login"),
    path('login/', CustomLoginView.as_view(), name="login"),

    # path('login/', v.login, name="login"),
    path('sns_login/<str:provider>', v.sns_login, name="sns_login"),

    path('signin_or_up/', v.signin_or_up, name="signin_or_up"),
    path('signup_choice/', v.signup_choice, name="signup_choice"),
    path('signup/', v.signup, name="signup"),
    path('check_email', v.check_email_dup, name="check_email_dup"),
    path('verify/<int:user_id>/<str:encrypted_code>', v.verify_auth_link, name="verify_auth_link"),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', v.password_change_done, name='password_change_done'),
    path('logout', v.logout, name="logout"),

    path('profile/save', v.profile_save, name="profile_save"),
]