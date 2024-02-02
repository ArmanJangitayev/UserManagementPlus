from django.urls import path


from .views import home_page, RegisterPageView, LoginPageView, logout, users_all, UserListView

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', RegisterPageView.as_view(), name='registration'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('test/', users_all, name='users_all'),
    path('users/', UserListView.as_view(), name='user-list'),

]
