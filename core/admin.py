from django.contrib import admin

# Custom imports
from core.models import (
    Subscriber,
    Contact,
    About,
    Team,
    Information,
)

admin.site.register([Subscriber, Contact, About, Team, Information])