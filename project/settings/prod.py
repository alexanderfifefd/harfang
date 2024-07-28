from .common import *  # noqa

DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

# Secure settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Trying to move debug stuff into this prod instance.
ENABLE_DEBUG_TOOLBAR = True

if DEBUG:
    if ENABLE_DEBUG_TOOLBAR:
        try:
            import debug_toolbar  # NOQA
        except ImportError:
            print("Failed to load debug_toolbar")
        else:
            INSTALLED_APPS.extend(["debug_toolbar"])
            MIDDLEWARE.insert(
                MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
                "debug_toolbar.middleware.DebugToolbarMiddleware",
            )
            INTERNAL_IPS = ["127.0.0.1"]
            # https://django-debug-toolbar.readthedocs.io/en/latest/tips.html#working-with-htmx-and-turbo
            DEBUG_TOOLBAR_CONFIG = {"ROOT_TAG_EXTRA_ATTRS": "hx-preserve"}

    try:
        import django_browser_reload  # NOQA
    except ImportError:
        print("Failed to load django_browser_reload")
    else:
        INSTALLED_APPS.extend(["django_browser_reload"])
        MIDDLEWARE.insert(
            MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
            "django_browser_reload.middleware.BrowserReloadMiddleware",
        )


# Add analytics
INSTALLED_APPS.append("analytics")

# Redis cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DATABASE_ROUTERS = ["project.settings.dbrouters.ClickHouseRouter"]

# ClickHouse database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.getenv("DATABASE_NAME", "db.sqlite3"),
    },
    "clickhouse": {
        "ENGINE": "clickhouse_backend.backend",
        "NAME": "default",
        "USER": "default",
        "PASSWORD": "",
        "HOST": os.getenv("CLICKHOUSE_HOST", "clickhouse"),
        "PORT": os.getenv("CLICKHOUSE_PORT", "9000"),
        "OPTIONS": {},
    },
}

# settings.py
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
