from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', include('base.urls')),
    path('learners/', include('learners.urls')),
    path('topics/', include('topics.urls')),
    path('admin/', admin.site.urls),
    path('accounts/',include('allauth.urls')),
]