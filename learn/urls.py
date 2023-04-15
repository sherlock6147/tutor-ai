from django.urls import path
from learn.views import *

app_name = 'learn'
urlpatterns = [
    path('<int:subtopic_id>/', learn_subtopic,name='learn_subtopic'),
    path('help/', show_help,name='help'),
    path('chat/<int:subtopic_id>/', chat_with_ai,name='chat_with_ai'),
]