"""pat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from pat import settings
from pat.views import home, serve
from refund.views import index, request_form, request_edit, request_approve, request_process

# pylint: disable=invalid-name
urlpatterns = [
    path('', home, name='home'),
    path("login/", auth_views.LoginView.as_view()),
    path("logout/", auth_views.LogoutView.as_view()),
    path('refund/', index, name='index'),
    path('refund/new/', request_form, name='request_form'),
    path('refund/edit/<int:request_id>/', request_edit, name='request_edit'),
    path('refund/approve/<int:request_id>/', request_approve, name='request_approve'),
    path('refund/process/<int:request_id>/', request_process, name='request_process'),
    path('admin/', admin.site.urls),
    re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve,
            kwargs={"document_root": settings.MEDIA_ROOT}),
]
