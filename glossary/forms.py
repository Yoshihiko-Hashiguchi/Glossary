from django import forms
from .models import Terms, Comments
import datetime

class TermCreateForm(forms.ModelForm):
    term = forms.CharField(label='用語')
    explanation = forms.CharField(label='説明', widget=forms.Textarea())
    picture = forms.ImageField(label='画像', required=False)
    
    class Meta:
        model = Terms
        fields = ('term', 'explanation', 'picture')


class TermUpdateForm(forms.ModelForm):
    term = forms.CharField(label='用語')
    explanation = forms.CharField(label='説明', widget=forms.Textarea())
    picture = forms.ImageField(label='画像', required=False)
    
    class Meta:
        model = Terms
        fields = ('term', 'explanation', 'picture')
    
    def save(self, commit=False):
        tern = super().save(commit=False)
        tern.update_at = datetime.datetime.now()
        tern.save() # User情報の保存
        return tern # 保存したデータを返す


class TermDeleteForm(forms.ModelForm):
    
    class Meta:
        model = Terms
        fields = []


class CommentsPostForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    
    class Meta:
        model = Comments
        fields = ('comment', )


class CommentsDeleteForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = []