from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from . import forms
from .auth import AuthSystem
from .cookie_manager import CookieManager
from django.shortcuts import render
from .dbmanager import SQLDBManager  # Предполагается, что ваш файл с классом находится в том же пакете
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


def home_page(request):
    return render(request, 'auth/main.html', {"request": request})


class LoginPageView(View):
    template_name = 'auth/login.html'
    form_class = forms.UserLoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = AuthSystem.authenticate_user(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                AuthSystem.login_user(request, username=form.cleaned_data['username'],
                                      password=form.cleaned_data['password'])

                response = redirect('home_page')
                response = CookieManager.set_cookie(response, 'logged_in', True)
                return response

            else:
                message = 'Invalid username or password'
        else:
            message = 'Login failed!'

        response = render(request, self.template_name, context={'form': form, 'message': message})
        return response


class RegisterPageView(View):
    template_name = 'auth/registration_page.html'
    form_class = forms.UserRegForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        print(form.data)
        user_id = None

        response = render(request, self.template_name, context={'form': form, 'message': message})

        if form.is_valid():
            user = AuthSystem.register_user(
                request,
                **form.cleaned_data,
            )
            user_id = user.id
            if user is not None:
                response = redirect('home_page')
                CookieManager.set_cookie_expiration(response, 'user_id', user_id, expiration_minutes=360)

            else:
                message = 'Registration failed!'
        return response


def logout(request):
    AuthSystem.logout_user(request)

    response = redirect('home_page')
    CookieManager.delete_cookie(response, 'logged_in')
    return response


def users_all(request):
    db_manager = SQLDBManager()

    db_manager.connect_to_db()

    query = "SELECT id, username, email FROM authorization_user"
    params = ['arman']
    result = db_manager.execute_query(query, params)

    for row in result:
        print(row)

    return render(request, 'auth/users.html', {"table": result})


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
