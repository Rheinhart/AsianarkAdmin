"""
AsianarkAdmin 配置（Python 3 / Django 6）。

设计要点
--------
* 所有环境相关项都走环境变量 / .env，代码里不留口令、不留主机名。
* 本地开发默认 sqlite + ASIANARK_MANAGED_TABLES=1（Django 建表，可跑测试、可造数）；
  连线上老库时设 ASIANARK_DB=mysql、ASIANARK_MANAGED_TABLES=0，模型全部 managed=False，
  Django 不碰表结构（老库的索引脚本见 docs/legacy_db_indexes.sql）。
* 时区 Asia/Shanghai —— 老配置是 UTC，导致后台显示的时间比实际早 8 小时。
"""
from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------------ .env（无第三方依赖）
def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


_load_dotenv(BASE_DIR / ".env")


def env_str(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in env_str(name, default).split(",") if item.strip()]


# ------------------------------------------------------------------ 基本
# 生产必须通过环境变量给；没给就用一个仅本机可用的开发密钥（DEBUG 模式）。
SECRET_KEY = env_str("ASIANARK_SECRET_KEY", "dev-only-insecure-key-do-not-use-in-production")
DEBUG = env_bool("ASIANARK_DEBUG", True)
ALLOWED_HOSTS = env_list("ASIANARK_ALLOWED_HOSTS", "*" if DEBUG else "")

ADMINS = [("Thomas", "thomas_lee@outlook.de")]

# ------------------------------------------------------------------ 应用
INSTALLED_APPS = [
    "AsianarkAdmin.admin_ext",          # 自定义 AdminSite / 分页 / 过滤器 / 统计条（无模型）
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "AsianarkAdmin.admin_ip_whitelist",
    "AsianarkAdmin.userinfo",
    "AsianarkAdmin.baccarat_Controll",
    "AsianarkAdmin.admin_log",
    # "AsianarkAdmin.serverinfo",       # 老项目里就是空的，保留注释便于以后启用
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 后台 IP 白名单（默认关闭，打开即生效；老配置里 key 拼错了，这里已对齐）
ADMIN_ACCESS_WHITELIST_ENABLED = env_bool("ASIANARK_IP_WHITELIST_ENABLED", False)
ADMIN_ACCESS_WHITELIST_MESSAGE = "Your ip address is not allowed!"
if ADMIN_ACCESS_WHITELIST_ENABLED:
    MIDDLEWARE.insert(0, "AsianarkAdmin.admin_ip_whitelist.middleware.AdminAccessIPWhiteListMiddleware")

ROOT_URLCONF = "AsianarkAdmin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 模板在项目自己的 templates/ 下，不再寄居在第三方包（suit）里
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "AsianarkAdmin.wsgi.application"

# ------------------------------------------------------------------ 数据库
DB_ENGINE = env_str("ASIANARK_DB", "sqlite")

if DB_ENGINE == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env_str("ASIANARK_DB_NAME", "bjl"),
            "USER": env_str("ASIANARK_DB_USER"),
            "PASSWORD": env_str("ASIANARK_DB_PASSWORD"),
            "HOST": env_str("ASIANARK_DB_HOST"),
            "PORT": env_str("ASIANARK_DB_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / env_str("ASIANARK_SQLITE_PATH", "bjl.sqlite3"),
        }
    }

# 业务表全部 managed=False（表结构属于老库）。本地开发用
# `python manage.py init_local_db` 在 sqlite 里建同样的表，线上不要跑。
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# ------------------------------------------------------------------ 缓存
MEMCACHE_LOCATION = env_str("ASIANARK_MEMCACHE_LOCATION")
if MEMCACHE_LOCATION and env_bool("ASIANARK_MEMCACHE_ENABLED", True):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            "LOCATION": MEMCACHE_LOCATION,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "asianark",
        }
    }

# ------------------------------------------------------------------ 游戏服 / 内存模型同步
GAME_SERVER = {
    "default": {
        "URL": env_str("ASIANARK_GAME_SERVER_URL", "127.0.0.1"),
        "PORT": env_str("ASIANARK_GAME_SERVER_PORT", "2012"),
        "NAME": env_str("ASIANARK_GAME_SERVER_NAME", "bjl_Game_Ser"),
        "TIMEOUT": env_int("ASIANARK_GAME_SERVER_TIMEOUT", 3),
        "ENABLED": env_bool("ASIANARK_PUSH_ENABLED", True),
    }
}

MEMCACHE = {
    "ENABLED": bool(MEMCACHE_LOCATION) and env_bool("ASIANARK_MEMCACHE_ENABLED", False),
    "LOCATION": MEMCACHE_LOCATION or "127.0.0.1:11211",
    "HOSTNAME": env_str("ASIANARK_MEMCACHE_HOSTNAME", "bjl"),
}

# 首页看板聚合结果的缓存时间（秒）
DASHBOARD_CACHE_SECONDS = env_int("ASIANARK_DASHBOARD_CACHE", 60)

# ------------------------------------------------------------------ 国际化 / 时区
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"          # ← 老配置是 UTC，所有时间显示差 8 小时
USE_I18N = True
USE_TZ = True

DATE_FORMAT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i:s"
DATE_INPUT_FORMATS = ["%Y-%m-%d"]
DATETIME_INPUT_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]

# ------------------------------------------------------------------ 静态文件
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ------------------------------------------------------------------ 安全 / 请求上限
# 分页参数是 GET 参数，不再靠 POST 塞全表主键（老写法会撞这个上限）。
DATA_UPLOAD_MAX_NUMBER_FIELDS = env_int("ASIANARK_MAX_NUMBER_FIELDS", 1000)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_FOR", "https")
    SESSION_COOKIE_SECURE = env_bool("ASIANARK_SESSION_COOKIE_SECURE", True)
    CSRF_COOKIE_SECURE = env_bool("ASIANARK_CSRF_COOKIE_SECURE", True)
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# ------------------------------------------------------------------ 日志（推送失败、缓存同步异常都要能查到）
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "loggers": {
        "asianark": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.contrib": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}
