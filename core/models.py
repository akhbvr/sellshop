from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(verbose_name='Email', max_length=50)
    is_active = models.BooleanField(verbose_name='Is active', default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subcribers'

    def __str__(self):
        return self.email


class Contact(models.Model):
    full_name = models.CharField(verbose_name='Full name', max_length=50)
    email = models.EmailField(verbose_name='Email', max_length=50)
    subject = models.CharField(verbose_name='Subject', max_length=150)
    message = models.TextField(verbose_name='Message')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.full_name


class About(models.Model):
    image = models.ImageField(verbose_name='Image', upload_to='core/about/')
    title = models.CharField(verbose_name='Title', max_length=50)
    description = models.TextField(verbose_name='Description')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'Abouts'

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(verbose_name='Name', max_length=20)
    image = models.ImageField(verbose_name='Image', upload_to='core/team/')
    url = models.CharField(verbose_name='URL', max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def __str__(self):
        return self.name


class Information(models.Model):
    location = models.CharField(verbose_name='Location', max_length=100)
    mail = models.EmailField(verbose_name='Mail', max_length=50)
    phone_number = models.CharField(verbose_name='Phone number', max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Information'
        verbose_name_plural = 'Informations'

    def __str__(self):
        return self.created_at


