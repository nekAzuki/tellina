"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from website import annotator, cmd2html, views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^translate', views.translate),
    url(r'^info$', views.info),

    url(r'^remember_ip_address$', views.remember_ip_address),
    url(r'^vote', views.vote),

    url(r'^login', annotator.login),
    url(r'^uri_panel', annotator.url_panel),
    url(r'^utility_panel', annotator.utility_panel),

    url(r'^explain_cmd$', cmd2html.explain_cmd),

    url(r'^admin', admin.site.urls)
]