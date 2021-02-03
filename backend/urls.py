from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView




# from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
# from rest_framework import viewsets

# from .models import Message, MessageSerializer


# # Serve Vue Application
# index_view = never_cache(TemplateView.as_view(template_name='index.html'))





urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include(('backend.base.urls', 'base'), namespace='base')),
    path('lexxer/', include('backend.apps.lexxer.urls')),
]


# catch-all for frontend
urlpatterns += [
    re_path('.*', never_cache(TemplateView.as_view(template_name='index.html'))),
]
