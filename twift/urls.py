from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.home, name='home'),
    url(r'^thanks/', TemplateView.as_view(template_name='twift/thanks.html'),
        name='thanks'),
    url(r'^availRide',views.avail_ride, name='avail_ride'),
    url(r'^offerNewRide/', views.offer_ride, name='offer_ride'),
]