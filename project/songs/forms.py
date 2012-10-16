from django import forms

from markitup.widgets import MarkItUpWidget

from project.songs.models import Song,Singer,Lyricist

class SongForm(forms.ModelForm):
    
    class Meta:
        model = Song
        fields = [
            "name",
            "lyric",
            "photo",
            "slug",
            'description',
            'singer',
            'lyricist',
        ]
        widgets = {
            "lyric": MarkItUpWidget(),
        }
        
class SingerForm(forms.ModelForm):
    
    class Meta:
        model = Singer
        fields = [
            "name",
            "description",
            "photo",
            "slug",
        ]
        
class LyricistForm(forms.ModelForm):
    
    class Meta:
        model = Lyricist
        fields = [
            "name",
            "description",
            "photo",
            "slug",
        ]