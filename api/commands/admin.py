from django.contrib import admin
from .models import Room, Player

admin.site.site_header = "MUD Admin"
admin.site.site_title = "MUD Admin Area"
admin.site.site_header = "Welcome to MUD Admin"

admin.site.register(Room)
admin.site.register(Player)
