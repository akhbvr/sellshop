from django import forms
from blogs.models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = (
            'comment',
            'parent',
        )

        widgets = {
            "comment": forms.Textarea(attrs={
                "placeholder": "Comment here...",
                "rows": "4"
            }),
            "parent": forms.HiddenInput()
        }