from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from account.models import Profile
from pytils.translit import slugify
from django_summernote.fields import SummernoteTextField


class Post(models.Model):
    class Category(models.TextChoices):
        TANK = 'TNK', 'Танк'
        DAMAGER = 'DMG', 'Разрушитель'
        HEALER = 'HLR', 'Целитель'
        TRADER = 'TRD', 'Торговец'
        GUILDMASTER = 'GLM', 'Гилдмастер'
        QUESTGIVER = 'QGR', 'Квестодатель'
        SMITH = 'SMT', 'Кузнец'
        TANNER = 'TNR', 'Кожевник'
        ALCHEMIST = 'ALC', 'Зельевар'
        WIZARD = 'WZD', 'Мастер заклинаний'

    title = models.CharField(max_length=150,
                             unique_for_date='created')
    slug = models.SlugField(max_length=150,
                            unique_for_date='created')
    content = SummernoteTextField()
    author = models.ForeignKey(to=Profile,
                               on_delete=models.CASCADE,
                               related_name='post')
    category = models.CharField(max_length=3,
                                choices=Category.choices)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateField(auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('news:post_detail',
                       args=[
                           self.created.year,
                           self.created.month,
                           self.created.day,
                           self.slug,
                       ])

    def get_absolute_url_for_profile(self):
        return reverse('news:profile-comments',
                       args=[
                           self.created.year,
                           self.created.month,
                           self.created.day,
                           self.slug,
                       ])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} {self.content[:30]}'


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(to=Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(to=Profile,
                               on_delete=models.CASCADE,
                               related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    objects = models.Manager()
    published = CommentManager()

    def __str__(self):
        return self.content[:30]