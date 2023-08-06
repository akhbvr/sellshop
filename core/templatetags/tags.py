from django.template import Library
from core.forms import ContactForm

register = Library()



@register.simple_tag
def get_contact_form():
    return ContactForm()


@register.simple_tag(name="get_total_amount")
def get_total_amount():
    pass