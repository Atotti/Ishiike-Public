import os
from pathlib import Path
import environ
import dj_database_url
from socket import gethostname

hostname = gethostname()
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env('.env')
SECRET_KEY = env('SECRET_KEY')

print("hostname", hostname)

if "DESKTOP-ABEN90S" in hostname: 
    DEBUG = True
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('LOCAL_DATABASES_NAME'),
        'USER': env('LOCAL_DATABASES_USER'),
        'PASSWORD': env('LOCAL_DATABASES_PASSWORD'),
        'HOST': env('LOCAL_DATABASES_HOST'),
        'PORT': env('LOCAL_DATABASES_PORT')
    },
    'subdb': {
        'ENGINE': 'django.db.backends.mysql', # データベースの種類設定
        'NAME': 'vac_rooms', 
        "USER": "dever",
        "PASSWORD": env('DB_PASSWORD'),
        "HOST": env('DB_HOST'),
        "PORT": "3306",
    }
    }
    ALLOWED_HOSTS = ["*"]
    print("ローカル環境")
else:
    DEBUG = False
    db_from_env = dj_database_url.config()
    DATABASES = {
        'default': dj_database_url.config(),
        'subdb': {
            'ENGINE': 'django.db.backends.mysql', # データベースの種類設定
            'NAME': 'vac_rooms', 
            "USER": "dever",
            "PASSWORD": env('DB_PASSWORD'),
            "HOST": env('DB_HOST'),
            "PORT": env('DB_PORT'),
        }
    }
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
    print("本番環境")

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'review',
    'accounts.apps.AccountsConfig',
    'rest_framework',
    'corsheaders',
    'django_ses',
    'search_syllabus.apps.SearchSyllabusConfig',
    'django_user_agents',
    'welcome.apps.WelcomeConfig',
    'api',
    'django.contrib.sites.apps.SitesConfig',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki.apps.WikiConfig',
    'wiki.plugins.attachments.apps.AttachmentsConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',
    'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.macros.apps.MacrosConfig',
    'wiki.plugins.editsection.apps.EditSectionConfig',
    'wiki.plugins.globalhistory.apps.GlobalHistoryConfig',
    'wiki.plugins.help.apps.HelpConfig',
    'wiki.plugins.links.apps.LinksConfig',
    'QandA',
    'django.contrib.postgres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'ishiike.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'welcome')], # wiki用のTEMPLTE_DIRの設定
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]


WSGI_APPLICATION = 'ishiike.wsgi.application'

EMAIL_BACKEND = 'django_ses.SESBackend'

AUTH_USER_MODEL = 'accounts.CustomUser'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ロギング
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        # diaryアプリケーションが利用するロガー
        'diary': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },

    # ハンドラの設定
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D',  # ログローテーション(新しいファイルへの切り替え)間隔の単位(D=日)
            'interval': 1,  # ログローテーション間隔(1日単位)
            'backupCount': 7,  # 保存しておくログファイル数
        },
    },

    # フォーマッタの設定
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

# django-wikiの設定
SITE_ID = 1

# メディアファイル関連1
MEDIA_URL = 'welcome/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'welcome/media')

#ログインした後のリダイレクト先
LOGIN_REDIRECT_URL = 'wiki:get'

WIKI_ACCOUNT_HANDLING = True
WIKI_ACCOUNT_SIGNUP_ALLOWED = False
