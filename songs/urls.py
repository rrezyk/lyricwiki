from django.conf.urls.defaults import *

urlpatterns = patterns('songs.views',
    (r'^(?P<song_slug>[-\w]+)/$', 'show_song', 
       {'template_name': 'songs/song.html'}, 'songs_song'),

)
