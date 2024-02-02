from django.contrib.auth import authenticate, login, logout

from .cookie_manager import CookieManager
from .models import User
from .session import SessionManager


class AuthSystem:
    @staticmethod
    def authenticate_user(request, username, password):
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        return False

    @staticmethod
    def login_user(request, username, password):
        user = authenticate(request, username=username, password=password)
        SessionManager.create_session(request, user)
        if user is not None:
            login(request, user)

    @staticmethod
    def register_user(request, **kwargs):
        password = kwargs['password1']
        del kwargs['password1']
        del kwargs['password2']
        user = User.objects.create_user(password=password, **kwargs)

        user.save()
        return user

    @staticmethod
    def logout_user(request):
        logout(request)

        SessionManager.destroy_session(request)
