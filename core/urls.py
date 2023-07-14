from django.urls import path
from core.views import ContactView, HomeView, AboutView


app_name = 'home'

urlpatterns = [
    # path("", home_page, name="home_page"),
    # path("contact/", contact_page, name="contact_page"),
    path("", HomeView.as_view(), name="home_page"),
    path("contact/", ContactView.as_view(), name="contact_page"),
    path("about/", AboutView.as_view(), name="about_page"),
]




    