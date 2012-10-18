# -*- coding: utf-8 -*-
from django.contrib import admin
from songs.models import Singer,Lyricist,Song


admin.site.register(Singer)
admin.site.register(Lyricist)
admin.site.register(Song)
