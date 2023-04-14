from django.contrib import admin
from topics.models import *

# Register your models here.
admin.site.register(Topic)
admin.site.register(SubTopic)