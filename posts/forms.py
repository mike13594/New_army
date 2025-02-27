from django import forms
from posts.models import Comment, Post
from seoul.models import Place

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]

        widgets = {
            "content" : forms.Textarea(
                attrs={
                    "placeholder": "댓글 달기  ",
                }
            )
        }

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
        ]
