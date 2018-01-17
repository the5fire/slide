from django.conf.urls import url

from .views import eventsource, ControlView, slide_view


urlpatterns = [
    url(r'(?P<slug>[\w\-\_]+)/event/$', eventsource, name='eventsource'),
    url(r'(?P<slug>[\w\-\_]+)/control/$', ControlView.as_view(), name='control'),
    url(r'(?P<slug>[\w\-\_]+)/$', slide_view, name='slide'),
]
