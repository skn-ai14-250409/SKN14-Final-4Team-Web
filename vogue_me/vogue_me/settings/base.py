import os
from pathlib import Path

# .env 로드 ######################################################
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR   = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure--b1q6+ymklxs)n#iqm5jlspl@=k-5$!r1hft=2_%nj27xbf!n3'
DEBUG      = True

# ALLOWED_HOSTS 설정  ############################################
ALLOWED_HOST  = os.getenv('ALLOWED_HOST', "127.0.0.1")
ALLOWED_HOSTS = [ALLOWED_HOST, ".looplabel.site", "127.0.0.1", "localhost"]

# 기본 Django 설정### ############################################
ROOT_URLCONF     = 'vogue_me.urls'
WSGI_APPLICATION = 'vogue_me.wsgi.application'
INSTALLED_APPS  = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "mainapp",
    "userapp",
    "mailapp",
    "apiapp",
]
MIDDLEWARE      = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
TEMPLATES       = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
DATABASES       = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE   = 'ko-kr'
TIME_ZONE       = 'Asia/Seoul'
USE_I18N        = True
USE_TZ          = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 정적 파일 ###########################################
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    # BASE_DIR / "userapp" / "static"
]

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / "media"


# 로그인 성공한 후의 리다이렉트 URL ( 기본값 = /accounts/profile )
LOGIN_URL = '/user/signin_or_up'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# SNS 로그인 및 메일 발송 ###########################################
NAVER_CLIENT_ID      = "oOGAmDASirYj7KTLf4ep"
NAVER_CLIENT_SECRET  = os.getenv("NAVER_CLIENT_SECRET")

KAKAO_CLIENT_ID      = "136499f4aaf7100f49322ab01e02eacc"
KAKAO_CLIENT_SECRET  = os.getenv("KAKAO_CLIENT_SECRET")

GOOGLE_CLIENT_ID     = "342938321475-m4385u4fem0ogd8jjr98bqdgdqk6q3j2.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your SMTP host
EMAIL_PORT = 465  # Or your SMTP port (e.g., 465 for SSL)
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")