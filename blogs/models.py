from django.db import models

# Custom imports
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='Category name', help_text='Max. 50 character.' ,max_length=50, db_index=True)

    parent = models.ForeignKey('self', verbose_name='Parent category', on_delete=models.CASCADE, related_name='parent_category', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag name', help_text='Max. 20 character.', max_length=20, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name='Post title', help_text='Max. 50 character.', max_length=50, db_index=True)
    short_description = models.CharField(verbose_name='Short description', help_text='Max. 100 character.', max_length=100)
    description = models.TextField(verbose_name='Description')
    main_image = models.ImageField(verbose_name='Main image', upload_to='blogs/post')
    cover_image = models.ImageField(verbose_name='Cover image', upload_to='blogs/post')
    slug = models.SlugField(null=True, blank=True, unique=True, editable=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author', related_name='post_author')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', related_name='post_tags')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category', related_name='post_category')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("single_post", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    


class Comment(models.Model):
    comment = models.TextField(verbose_name='Comment')

    parent = models.ForeignKey("self",verbose_name='Parent comment', on_delete=models.CASCADE, related_name='parent_comment', null=True, blank=True)
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE, related_name='post')
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE, related_name='comment_author')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment + "----" + self.post.title + "----" + self.author.first_name


