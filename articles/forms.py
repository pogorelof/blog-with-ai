from django import forms
from .models import Article, Comment

input_class = 'text-black w-full p-2 rounded-xl outline-none h-28 resize-none'
# image_class = 'file:bg-gray-100 hover:file:bg-gray-200 file:cursor-pointer file:border-none file:rounded-lg file:p-2 border border-1 border-white rounded-xl bg-white'
image_class = 'hidden'

class ArticleForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'class':input_class, 'id':'textArea'}), max_length=300)
    photo = forms.ImageField(label='', required=False,widget=forms.FileInput(attrs={'class': image_class, 'id': 'fileinput'}))
    class Meta:
        model = Article
        fields = ['body', 'photo']
        
class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'class':input_class}))
    class Meta:
        model = Comment
        fields = ['body']