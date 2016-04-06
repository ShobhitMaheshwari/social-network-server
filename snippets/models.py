from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth.models import User


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='snippets')

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        super(Snippet, self).save(*args, **kwargs)


class Friendship(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    approved = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name="friends")
    friend = models.ForeignKey(User, related_name="friend_id")