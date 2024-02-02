import secrets
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.utils import timezone


class SessionManager:
    @staticmethod
    def create_session(request, user=None):
        request.session['username'] = user.username
        request.session['email'] = user.email
        request.session['name'] = user.name

    @staticmethod
    def destroy_session(request):
        if 'username' in request.session:
            del request.session['username']
        if 'email' in request.session:
            del request.session['email']
        if 'name' in request.session:
            del request.session['name']


