from django.urls import path

# Custom imports
from blogs.views import posts, single_post, liked_post, PostsListView, PostDetailView


app_name = 'blogs'

urlpatterns = [
    # path('', posts, name='posts'),
    path('', PostsListView.as_view(), name='posts'),
    # path('<slug:slug>', single_post, name='single_post'),
    path('<slug:slug>', PostDetailView.as_view(), name='single_post'),
    path('liked-post/<int:pk>', liked_post, name='liked_post'),
]
