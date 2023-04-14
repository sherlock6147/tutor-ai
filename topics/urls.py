from django.urls import path
from topics.views import *

app_name = 'topics'
urlpatterns = [
    path('', all_topics,name='all_topics'),
    path('add/', add_topic,name='add_topic'),
    path('edit/<int:topic_id>', edit_topic,name='edit_topic'),
    path('edit_subtopic/<int:subtopic_id>', edit_subtopic,name='edit_subtopic'),
    path('delete/<int:topic_id>', delete_topic,name='delete'),
    path('delete_subtopic/<int:subtopic_id>', delete_subtopic,name='delete_subtopic'),
    path('add_subtopic/<int:topic_id>', add_subtopic,name='add_subtopic'),
]