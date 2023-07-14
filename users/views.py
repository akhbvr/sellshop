from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth import get_user_model
from users.forms import RegisterForm, LoginForm, ShippingAddressForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from users.tasks import send_confirmation_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from users.tokens import account_activatioin_token
from django.views.generic import CreateView, TemplateView
from django.views import View
from orders.models import ShippingAddress

User = get_user_model()

# @login_required(login_url="users:login")
def my_account(request):

    return render(request, 'my-account.html')


class MyAccountView(TemplateView):
    template_name = 'my-account.html'
    def get(self, request):
        try:
            profile = User.objects.get(username=request.user.username)
            profile_form = ProfileForm(initial={
                'bio': profile.bio,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'username': profile.username,
                'email': profile.email
            })

            shipping_address = ShippingAddress.objects.filter(customer=request.user).first()
            form = ShippingAddressForm(initial={
                'line_1': shipping_address.line_1,
                'line_2': shipping_address.line_2,
                'address': shipping_address.address,
                'postal_code': shipping_address.postal_code,
                'country': shipping_address.country,
                'city': shipping_address.city
            })
            return render(request, 'my-account.html', {"form": form, "profile_form": profile_form})
        except:
            form = ShippingAddressForm()
            profile_form = ProfileForm()
            return render(request, 'my-account.html', {"form": form, "profile_form": profile_form})
        
        
    def post(self, request):
        if request.POST.get('is_shipping_address') != None:
            try:
                shipping_address = ShippingAddress.objects.filter(customer=request.user).first()
                form = ShippingAddressForm(data=request.POST)
                if form.is_valid():
                    shipping_address.line_1 = form.cleaned_data['line_1']
                    shipping_address.line_2 = form.cleaned_data['line_2']
                    shipping_address.address = form.cleaned_data['address']
                    shipping_address.postal_code = form.cleaned_data['postal_code']
                    shipping_address.country = form.cleaned_data['country']
                    shipping_address.city = form.cleaned_data['city']
                    shipping_address.customer = request.user
                    shipping_address.save()
                    return redirect(reverse_lazy('users:my_account'))
                else:
                    return render(request, 'my-account.html', {"form": form})
            except:
                form = ShippingAddressForm(data=request.POST)
                if form.is_valid():
                    shipping_address = form.save(commit=False)
                    shipping_address.customer = request.user
                    shipping_address.save()
                    return redirect(reverse_lazy('users:my_account'))
                else:
                    return redirect(request, 'my-account.html', {"form": form})

        if request.POST.get('is_profile') != None:
            try:
                profile = User.objects.get(username=request.user.username)
                form = ProfileForm(data=request.POST, files=request.FILES)
                print("\n\n\n\n\n\n\n\n\n\n",form.is_valid() ,"\n\n\n\n\n\n\n")
                if form.is_valid():
                    profile.bio = request.POST.get('bio')
                    profile.first_name = request.POST.get('first_name')
                    profile.last_name = request.POST.get('last_name')
                    profile.email = request.POST.get('email')
                    profile.image = request.FILES.get('image')
                    profile.save()
                    return redirect(reverse_lazy('users:my_account'))
                else:
                    return redirect(reverse_lazy('users:my_account'))
            except:
                form = ProfileForm(data=request.POST, files=request.FILES)
                if form.is_valid():
                    form.save()
                    return redirect(reverse_lazy('users:my_account'))
                else:
                    return redirect(reverse_lazy('users:my_account'))


def login(request):
    if request.user.is_authenticated:
        return redirect('home:home_page')
    
    register_form = RegisterForm()
    login_form = LoginForm()
    
    if request.method == 'POST':

        if request.POST.get('is_register') != None:
            register_form = RegisterForm(data=request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                current_site = get_current_site(request)
                send_confirmation_mail(user, current_site) 
                return redirect(reverse_lazy("users:login"))
            else:
                context = {
                    "register_form": register_form,
                    "login_form": login_form
                }
                return render(request, 'login.html', context)
            
        if request.POST.get('is_login') != None:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():

                user = authenticate(request=request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
                if user:
                    login_auth(request, user)
                    next_page = request.GET.get('next', reverse_lazy("home:home_page"))
                    return redirect(next_page)
                
                messages.add_message(request, messages.ERROR, 'User not found')


    context = {
        "register_form": register_form,
        "login_form": login_form
    }
    return render(request, 'login.html', context)
    
    
def logout(request):
    logout_auth(request)
    return redirect('users:login')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activatioin_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse_lazy('users:login'))
    else:
        return redirect(reverse_lazy('home:home_page'))