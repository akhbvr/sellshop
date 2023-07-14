from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from orders.models import ShippingAddress


User = get_user_model()

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        )

        widgets = {
            'first_name': forms.TextInput(attrs={
                "placeholder": "First name here.."
            }),
            'last_name': forms.TextInput(attrs={
                "placeholder": "Last name here.."
            }),
            'username': forms.TextInput(attrs={
                "placeholder": "Username here.."
            }),
            'email': forms.EmailInput(attrs={
                "placeholder": "Email Address.."
            }),
            'password': forms.PasswordInput(attrs={
                "placeholder": "Password"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            print("\n\n\nburdayam\n\n\n")
            self.add_error('confirm_password', 'Password and Confirm password is not same!')
            raise ValidationError("Password and Confirm password is not same!")

    
    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.save()
        return user
    

class LoginForm(forms.Form):

    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        "placeholder": "Username here.."
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Password.."
    }))


class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress

        fields = (
            'line_1',
            'line_2',
            'address',
            'postal_code',
            'country',
            'city',
        )

        widgets = {
            'line_1': forms.TextInput(attrs={
                "placeholder": "Line 1 here..",
            }),
            'line_2': forms.TextInput(attrs={
                "placeholder": "Line 2 here..",
            }),
            'address': forms.TextInput(attrs={
                "placeholder": "Address here..",
            }),
            'postal_code': forms.TextInput(attrs={
                "placeholder": "Postal code here..",
            }),
            'country': forms.Select(attrs={
                "placeholder": "Country here..",
                "style": "padding: 10px 20px; border: none; background: rgba(0,0,0,0.04)"
            }),
            'city': forms.TextInput(attrs={
                "placeholder": "City here..",
            })
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = (
            'image',
            'bio',
            'first_name',
            'last_name',
            'email',
        )

        widgets = {
            'image': forms.FileInput(attrs={
                "style": "padding: 10px 20px; border: none; background: rgba(0,0,0,0.04); width: 100%;"
            }),
            'bio': forms.Textarea(attrs={
                "placeholder": "Bio here..",
                "style": "padding: 10px 20px; border: none; background: rgba(0,0,0,0.04); width: 100%; resize: none;",
                "rows": "4",
            }),
            'first_name': forms.TextInput(attrs={
                "placeholder": "First name here..",
                "style": "padding: 10px 20px; border: none; background: rgba(0,0,0,0.04); width: 100%;"
            }),
            'last_name': forms.TextInput(attrs={
                "placeholder": "Last name here..",
                "style": "padding: 10px 20px; border: none; background: rgba(0,0,0,0.04); width: 100%;"
            }),
            'email': forms.EmailInput(attrs={
                "placeholder": "Email Address..",
                "style": "padding: 10px 20px; border: none; background: rgba(0,0,0,0.04); width: 100%;"
            })
        }
