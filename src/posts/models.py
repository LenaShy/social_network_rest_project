import os

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify


from markdown_deux import markdown

from .utils import get_read_time

User = settings.AUTH_USER_MODEL


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(publish__lte=timezone.now())


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = instance.slug
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return '{new_filename}/{final_filename}'.format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class Post(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path,
                              null=True,
                              blank=True)
    content = models.TextField()
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_api_like_url(self):
        return reverse("posts-api:like", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-updated", ]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "{0}-{1}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)

