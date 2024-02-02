from django.urls import path


from .views import upload_file

urlpatterns = [
    path('files/', upload_file, name='files/'),

]
