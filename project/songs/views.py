# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.decorators import login_required


from project.songs.models import Song




def show_song(request, song_slug, template_name="songs/song.html"):
    print song_slug
    print 'here'
    song = get_object_or_404(Song, slug=song_slug)
    page_title = song.name
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
