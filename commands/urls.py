from django.conf.urls import url
from . import api

urlpatterns = [
    url('create', api.generate_world),
    url('init', api.initialize),
    url('map', api.get_map),
    url('move', api.move),
    url('take', api.take),
    url('drop', api.drop),
    url('say', api.say)
]
