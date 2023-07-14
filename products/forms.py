from django import forms
from products.models import Review

class CommentForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = (
            'rating',
            'comment',
        )

        widgets = {
            "rating": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={
                "placeholder": "Comment here...",
                "rows": "4"
            }),
        }