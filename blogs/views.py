from typing import Any, Dict
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from blogs.models import (
    Category,
    Tag,
    Post,
    Comment
)
from products.models import (
    Brand,
)

from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from blogs.forms import CommentForm


def posts(request):
    posts = Post.objects.all().order_by("-created_at")
    categories = Category.objects.all()
    tags = Tag.objects.all()
    print("\n\n\n",request.session.get('liked_posts'),"\n\n\n")
    context = {
        "posts": posts,
        "categories": categories,
        "tags": tags
    }
    return render(request, 'blog.html', context=context)


class PostsListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    ordering = ("-created_at",)
    paginate_by = 1


def single_post(request, slug):
    post = Post.objects.get(slug=slug)
    brands = Brand.objects.all().order_by("-created_at")[:5]
    categories = Category.objects.all()
    posts = Post.objects.all().order_by("-created_at")[:3]
    comment_count = Comment.objects.filter(post=post).count()
    context = {
        "post": post,
        "brands": brands,
        "categories": categories,
        "posts": posts,
        "comment_count": comment_count
    }
    if request.method == 'POST':
        if "sub_comment" not in request.POST and request.POST['comment'] != "":
            comment = request.POST['comment']
            user = request.user
            new_comment = Comment.objects.create(comment=comment, post=post, author=user)
            new_comment.save()

        if "sub_comment" in request.POST and request.POST['sub_comment'] != "":
            parent_comment = request.POST['parent_comment']
            sub_comment = request.POST['sub_comment']
            user = request.user
            new_comment = Comment.objects.create(comment=sub_comment, parent_id=parent_comment, post=post, author=user)

        return redirect('blogs:single_post', slug=slug)
    return render(request, 'single-blog.html', context)


class PostDetailView(FormMixin ,DetailView):
    form_class = CommentForm
    model = Post
    template_name = "single-blog.html"

    def get_success_url(self):
        return reverse_lazy("blogs:single_post", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all().order_by("-created_at")[:5]
        context['categories'] = Category.objects.all()
        context['posts'] = Post.objects.all().order_by("-created_at")[:3]
        context['form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)
    


def liked_post(request, pk):
    messages.add_message(request, messages.SUCCESS, 'Beyenildi!')
    request.session['liked_posts'] = request.session.get('liked_posts', '') + str(pk) + ' '
    return redirect('blogs:posts')


# def liked_post(request, pk):
#     messages.add_message(request, messages.SUCCESS, 'Beyenildi!')
#     response = HttpResponse('bruh')
#     response.set_cookie('liked_posts', request.COOKIES.get('liked_posts', '') + str(pk) + ' ')

#     return response

