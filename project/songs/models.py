from django.db import models

class Singer(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    class Meta:
        db_table = 'singers'
        ordering = ['name']
        
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('lyric_singer', (), { 'singer_slug': self.slug })
        
class Lyricist(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    class Meta:
        db_table = 'lyricists'
        ordering = ['name']
        
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('lyric_lyricist', (), { 'lyricist_slug': self.slug })
        
class Song(models.Model):
    name=models.CharField(max_length=100)
    lyric=models.TextField()
    slug=models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    singer=models.ForeignKey(Singer)
    lyricist=models.ForeignKey(Lyricist)
    class Meta:
        db_table = 'songs'
        ordering = ['name']
        
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('lyric_song', (), { 'song_slug': self.slug })
