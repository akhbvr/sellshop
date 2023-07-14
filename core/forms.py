from django import forms
from core.models import Contact



class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact

        fields = (
            'full_name',
            'email',
            'subject',
            'message',
        )

        widgets = {
            "full_name": forms.TextInput(attrs={
                "placeholder": "Enter your Name...",
                "style": "width: 100%;"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter your email...",
                "style": "width: 100%; margin-bottom: 10px;"
            }),
            "subject": forms.TextInput(attrs={
                "placeholder": "Enter subject...",
                "style": "width: 100%;"
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Enter your message....",
                "style": "width: 100%;",
                "rows": "5"
            })
        }