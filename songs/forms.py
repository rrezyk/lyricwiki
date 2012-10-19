from django import forms
from markitup.widgets import MarkItUpWidget
from songs.models import Song,Singer,Lyricist


class BasicForm(forms.ModelForm):

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value


class SongForm(BasicForm):
    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.fields["singer"] = forms.ModelChoiceField(
            queryset = Singer.objects.order_by("name")
        )
        self.fields["lyricist"] = forms.ModelChoiceField(
            queryset = Lyricist.objects.order_by("name")
        )
    class Meta:
        model = Song
        fields = [
            "name",
            "lyric",
            "photo",
            'description',
            'singer',
            'lyricist',
        ]
        widgets = {
            "lyric": MarkItUpWidget(),
        }
        
class SingerForm(BasicForm):
    
    class Meta:
        model = Singer
        fields = [
            "name",
            "description",
            "photo",
        ]
        
class LyricistForm(BasicForm):
    
    class Meta:
        model = Lyricist
        fields = [
            "name",
            "description",
            "photo",
        ]
