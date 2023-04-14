from django.urls import path
from learners.views import *

app_name = 'learners'
urlpatterns = [
    path('profile/', profile,name='profile'),
    path('register/', register,name='register'),
]