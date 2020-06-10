from django.forms import ModelForm

from information_page.models import (
    ArticleComment,
    ArticleNote
)

class CommentForm(ModelForm):

    class Meta:
        model = ArticleComment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)
        self.fields['text'].label = 'Comment'

class NoteForm(ModelForm):

    class Meta:
        model = ArticleNote
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)
        self.fields['text'].label = 'Note about the article'
