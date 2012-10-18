from django.db import models
from django.utils.translation import ugettext_lazy as _
from markitup.fields import MarkupField
from django.contrib.auth.models import User
import datetime
"""
class Article(models.Model):
    name = models.CharField(max_length=100,blank=False)
    slug=models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add =True)
    locked = models.BooleanField(default=False, verbose_name=_('Locked for editing'))
    permissions = models.ForeignKey('Permission', verbose_name=_('Permissions'),
                                    blank=True, null=True,
                                    help_text=_('Permission group'))
    current_revision = models.OneToOneField('Revision', related_name='current_rev',
                                            blank=True, null=True, editable=True)
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name
        
    def can_read(self, user):
        if self.permissions:
            perms = self.permissions.can_read.all()
            return perms.count() == 0 or (user in perms)
        else:
            return self.parent.can_read(user) if self.parent else True

    def can_write(self, user):
        if self.permissions:
            perms = self.permissions.can_write.all()
            return perms.count() == 0 or (user in perms)
        else:
            return self.parent.can_write(user) if self.parent else True

    def can_write_l(self, user):
        return not self.locked and self.can_write(user)

class Singer(Article):
    photo = models.ImageField(upload_to="singer_photos", blank=True)
    
    class Meta:
        abstract = False
        db_table = 'singers'
        ordering = ['name']
        
    def save(self, *args, **kwargs):
        super(Singer, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str(self.id)
            self.save()
            

    @models.permalink
    def get_absolute_url(self):
        return ('lyric_singer', (), { 'singer_slug': self.slug })
        
class Lyricist(Article):
    photo = models.ImageField(upload_to="lyricist_photos", blank=True)

    class Meta:
        abstract = False
        db_table = 'lyricists'
        ordering = ['name']
        
    def save(self, *args, **kwargs):
        super(Lyricist, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str(self.id)
            self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('lyric_lyricist', (), { 'lyricist_slug': self.slug })
        
class Song(Article):

    lyric= MarkupField(blank=True, help_text="Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>.")
    photo = models.ImageField(upload_to="song_photos", blank=True)

    singer=models.ForeignKey(Singer)
    lyricist=models.ForeignKey(Lyricist)


                                        
    class Meta:
        abstract = False
        db_table = 'songs'
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(Song, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = str(self.id)
            self.save()
            
    
    @models.permalink
    def get_absolute_url(self):
        return ('lyric_song', (), { 'song_slug': self.slug })
        
class Revision(models.Model):
    
    article = models.ForeignKey(Article, verbose_name=_('Article'))
    revision_text = models.CharField(max_length=255, blank=True, null=True, 
                                     verbose_name=_('Description of change'))
    revision_user = models.ForeignKey(User, verbose_name=_('Modified by'), 
                                      blank=True, null=True, related_name='wiki_revision_user')
    revision_date = models.DateTimeField(auto_now_add = True, verbose_name=_('Revision date'))
    contents = models.TextField(verbose_name=_('Contents (Use MarkDown format)'))
    contents_parsed = models.TextField(editable=False, blank=True, null=True)
    counter = models.IntegerField(verbose_name=_('Revision#'), default=1, editable=False)
    previous_revision = models.ForeignKey('self', blank=True, null=True, editable=False)
    
    def get_user(self):
        return self.revision_user if self.revision_user else _('Anonymous')
    
    def save(self, **kwargs):
        if self.article and self.article.current_revision:
            if self.article.current_revision.contents == self.contents:
                return
            else:
                self.article.modified_on = datetime.datetime.now()
                self.article.save()
        
        # Increment counter according to previous revision
        previous_revision = Revision.objects.filter(article=self.article).order_by('-counter')
        if previous_revision.count() > 0:
            if previous_revision.count() > previous_revision[0].counter:
                self.counter = previous_revision.count() + 1
            else:
                self.counter = previous_revision[0].counter + 1
        else:
            self.counter = 1
        self.previous_revision = self.article.current_revision

        # Create pre-parsed contents - no need to parse on-the-fly
        ext = WIKI_MARKDOWN_EXTENSIONS
        ext += ["wikilinks(base_url=%s/)" % reverse('wiki_view', args=('',))]
        self.contents_parsed = markdown(self.contents,
                                        extensions=ext,
                                        safe_mode='escape',)
        super(Revision, self).save(**kwargs)
        
    def delete(self, **kwargs):

        article = self.article
        if article.current_revision == self:
            prev_revision = Revision.objects.filter(article__exact = article,
                                                    pk__not = self.pk).order_by('-counter')
            if prev_revision:
                article.current_revision = prev_revision[0]
                article.save()
            else:
                r = Revision(article=article, 
                             revision_user = article.created_by)
                r.contents = unicode(_('Auto-generated stub'))
                r.revision_text= unicode(_('Auto-generated stub'))
                r.save()
                article.current_revision = r
                article.save()
        super(Revision, self).delete(**kwargs)
    
    def get_diff(self):
        if self.previous_revision:
            previous = self.previous_revision.contents.splitlines(1)
        else:
            previous = []
        
        # Todo: difflib.HtmlDiff would look pretty for our history pages!
        diff = difflib.unified_diff(previous, self.contents.splitlines(1))
        # let's skip the preamble
        diff.next(); diff.next(); diff.next()
        
        for d in diff:
            yield d
    
    def __unicode__(self):
        return "r%d" % self.counter

    class Meta:
        verbose_name = _('article revision')
        verbose_name_plural = _('article revisions')

class Permission(models.Model):
    permission_name = models.CharField(max_length = 255, verbose_name=_('Permission name'))
    can_write = models.ManyToManyField(User, blank=True, null=True, related_name='write',
                                       help_text=_('Select none to grant anonymous access.'))
    can_read = models.ManyToManyField(User, blank=True, null=True, related_name='read',
                                       help_text=_('Select none to grant anonymous access.'))
    def __unicode__(self):
        return self.permission_name
    class Meta:
        verbose_name = _('Article permission')
        verbose_name_plural = _('Article permissions')

class RevisionForm(forms.ModelForm):
    contents = forms.CharField(label=_('Contents'), widget=forms.Textarea(attrs={'rows':8, 'cols':50}))
    class Meta:
        model = Revision
        fields = ['contents', 'revision_text']
class RevisionFormWithTitle(forms.ModelForm):
    title = forms.CharField(label=_('Title'))
    class Meta:
        model = Revision
        fields = ['title', 'contents', 'revision_text']
class CreateArticleForm(RevisionForm):
    title = forms.CharField(label=_('Title'))
    class Meta:
        model = Revision
        fields = ['title', 'contents',]

def set_revision(sender, *args, **kwargs):

    instance = kwargs['instance']
    created = kwargs['created']
    if created and instance.article:
        instance.article.current_revision = instance
        instance.article.save()

signals.post_save.connect(set_revision, Revision)

"""

from django.db import models
from markitup.fields import MarkupField
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
