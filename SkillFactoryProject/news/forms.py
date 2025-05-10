from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Post, Comment



# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'category',]
#         labels = {
#             'title': 'Заголовок',
#             'category': 'Категория',
#             'content': 'Текст',
#         }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=['title', 'content', 'category']
        labels = {
            'title': 'Заголовок',
            'category': 'Категория',
            'content': 'Текст',
        }
        widgets = {
            'content': SummernoteWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets={
            'content': forms.TextInput(attrs={'placeholder':'Комментарий'})
        }
