from django.urls import path, re_path
from users.views import login, logout, activate, MyAccountView

app_name = "users"

urlpatterns = [
    # path('register', register, name="register"),
    # path('my_account', my_account, name="my_account"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('my_account', MyAccountView.as_view(), name="my_account"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$', activate, name='activate'),
]
