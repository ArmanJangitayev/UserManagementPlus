# cookie_manager.py
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone


class CookieManager:
    @staticmethod
    def set_cookie(response, key, value, secure=False, httponly=False, expiration=None):
        response.set_cookie(key, value, secure=secure, httponly=httponly, expires=expiration)
        return response

    @staticmethod
    def get_cookie(request, key):
        return request.COOKIES.get(key)

    @staticmethod
    def set_cookie_expiration(response, key, value, expiration_minutes=60, secure=False, httponly=False):
        expiration = timezone.now() + timezone.timedelta(minutes=expiration_minutes)
        CookieManager.set_cookie(response, key, value, secure=secure, httponly=httponly, expiration=expiration)
        return response

    @staticmethod
    def ensure_cookie_security(response, key):
        response.set_cookie(key, secure=True)
        return response

    @staticmethod
    def set_cookie_secure(response, key, value):
        return CookieManager.set_cookie(response, key, value, secure=True)

    @staticmethod
    def delete_cookie(response, key):
        response.delete_cookie(key)
        return response
