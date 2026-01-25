"""
Django settings for LibraryProject project.

Security Best Practices Implementation:
- DEBUG mode disabled for production
- Secure cookies configuration
- Browser security headers
- CSRF protection
- Content Security Policy
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
# TODO: Move to environment variable in production
SECRET_KEY = "django-insecure-)_q=66=y!%m(wmxir2iv_f3e!=&n)w-)&y8=#5os3an*ww#r*9"

# SECURITY WARNING: don't run with debug turned on in production!
# Set to False in production to prevent exposure of sensitive information
DEBUG = False

# Define allowed hosts to prevent HTTP Host header attacks
# Add your domain names here in production
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".yourdomain.com"]


# ==============================================================================
# SECURITY MIDDLEWARE AND HEADERS
# ==============================================================================

# Security middleware should be at the top of the list
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Must be first
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking protection
]

# ==============================================================================
# BROWSER SECURITY HEADERS
# ==============================================================================

# Prevent browsers from MIME-sniffing a response away from the declared content type
# Helps prevent XSS attacks
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable browser's built-in XSS protection
# Helps prevent cross-site scripting attacks
SECURE_BROWSER_XSS_FILTER = True

# Prevent the site from being displayed in a frame/iframe
# Protects against clickjacking attacks
# Options: 'DENY', 'SAMEORIGIN', or 'ALLOW-FROM uri'
X_FRAME_OPTIONS = "DENY"

# ==============================================================================
# HTTPS AND SECURE COOKIES
# ==============================================================================

# Ensure CSRF cookie is only sent over HTTPS
# Set to True in production with HTTPS
CSRF_COOKIE_SECURE = True

# Ensure session cookie is only sent over HTTPS
# Set to True in production with HTTPS
SESSION_COOKIE_SECURE = True

# Redirect all HTTP requests to HTTPS
# Enable in production with HTTPS configured
SECURE_SSL_REDIRECT = True

# How long (in seconds) the browser should remember to only access via HTTPS
# 1 year = 31536000 seconds
SECURE_HSTS_SECONDS = 31536000

# Include all subdomains in HSTS policy
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Allow the site to be preloaded in browsers' HSTS lists
SECURE_HSTS_PRELOAD = True

# ==============================================================================
# CSRF PROTECTION
# ==============================================================================

# Use a secure session cookie for CSRF
CSRF_USE_SESSIONS = True

# Only allow CSRF cookies to be sent from same site
CSRF_COOKIE_HTTPONLY = True

# Same-site cookie attribute for CSRF cookie
# Options: 'Strict', 'Lax', or None
CSRF_COOKIE_SAMESITE = "Strict"

# ==============================================================================
# SESSION SECURITY
# ==============================================================================

# Prevent client-side JavaScript from accessing session cookies
SESSION_COOKIE_HTTPONLY = True

# Same-site cookie attribute for session cookie
SESSION_COOKIE_SAMESITE = "Strict"

# Session timeout (in seconds) - 2 weeks
SESSION_COOKIE_AGE = 1209600

# Expire session when browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ==============================================================================
# CONTENT SECURITY POLICY
# ==============================================================================

# Content Security Policy to prevent XSS attacks
# Restricts sources from which content can be loaded
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = ("'self'",)

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bookshelf",
    "relationship_app",
]

ROOT_URLCONF = "LibraryProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LibraryProject.wsgi.application"

# Custom User Model
AUTH_USER_MODEL = "bookshelf.CustomUser"

# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,  # Require at least 8 characters
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC AND MEDIA FILES
# ==============================================================================

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# DEVELOPMENT SETTINGS OVERRIDE
# ==============================================================================

# For development, you can override some security settings
# Remove or comment out these lines in production
if DEBUG:
    # Allow development without HTTPS
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

    # Add more permissive CSP for development
    CSP_SCRIPT_SRC = (
        "'self'",
        "'unsafe-inline'",
        "'unsafe-eval'",
        "https://cdnjs.cloudflare.com",
    )
