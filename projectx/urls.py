"""projectx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
<<<<<<< HEAD
import allauth
from django.conf.urls import include,url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()
=======
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from twift.forms import LoginForm
>>>>>>> 05bb589620131d4dae37299df6484db41d3fd395

urlpatterns = [
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
<<<<<<< HEAD
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', TemplateView.as_view(template_name='account/profile.html')),
	
=======
    url(r'^twift/', include('twift.urls')),
    #url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}),
    #url(r'^logout/$', views.logout, {'next_page': '/login'}),
    url(r'^accounts/', include('registration.backends.default.urls')),
>>>>>>> 05bb589620131d4dae37299df6484db41d3fd395
]
