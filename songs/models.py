from django.db import models
from django.utils.translation import ugettext_lazy as _
from markitup.fields import MarkupField
from django.contrib.auth.models import User
import datetime

class Singer(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="singer_photos", blank=True)
    created = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False
    )
    class Meta:
        db_table = 'singers'
        ordering = ['name']
        
    def save(self, *args, **kwargs):
        super(Singer, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str(self.id)
            self.save()
            
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('lyric_singer', (), { 'singer_slug': self.slug })
        
class Lyricist(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="lyricist_photos", blank=True)
    created = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False
    )
    class Meta:
        db_table = 'lyricists'
        ordering = ['name']
        
    def save(self, *args, **kwargs):
        super(Lyricist, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str(self.id)
            self.save()
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('lyric_lyricist', (), { 'lyricist_slug': self.slug })
        
class Song(models.Model):
    name=models.CharField(max_length=100)
    lyric= MarkupField(blank=True, help_text="Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>.")
    slug=models.SlugField(max_length=100, unique=True)
    photo = models.ImageField(upload_to="song_photos", blank=True)
    description = models.TextField()
    singer=models.ForeignKey(Singer)
    lyricist=models.ForeignKey(Lyricist)
    created = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False
    )
    class Meta:
        db_table = 'songs'
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(Song, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str(self.id)
            self.save()
            
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('lyric_song', (), { 'song_slug': self.slug })
        

