from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from core.forms import ContactForm
from django.contrib import messages
from django.views.generic import CreateView, TemplateView


class AboutView(TemplateView):
    template_name = 'about.html'


def home_page(request):
    return  render(request, "index.html")


class HomeView(TemplateView):
    template_name = 'index.html'


def contact_page(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Formunuz gonderildi!')
            return redirect(reverse_lazy("home:contact_page"))
        return render(request, 'contact.html', {"form": form})
    return render(request, 'contact.html', {"form": form})


class ContactView(CreateView):
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy("home:contact_page")

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Formunuz gonderildi!')
        return super().form_valid(form)