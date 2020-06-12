from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


from tools.models import (
    Comment,
    Entry,
    Genre
)


# Create your models here.
class ArticleGenre(Genre):

    def get_absolute_url(self):
        return reverse('informations:genre-details',
                       kwargs={'slug': self.slug})

    def publicated_articles(self):
        return self.article_set.filter(published=True).count()


class Article(Entry):
    genre = models.ForeignKey(ArticleGenre,
                              on_delete=models.CASCADE)
    last_modification_date = models.DateTimeField(blank=True, null=True)
    publication_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ('can_publish', 'Can publish article'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.published:
            self.publication_date = datetime.now()
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('informations:article-details',
                       kwargs={'slug': self.slug})

    def publish(self):
        self.publication_date = datetime.now()
        self.published = True
        self.save()


class ArticleComment(Comment):
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='comments',
                                editable=False)

    def get_absolute_url(self):
        return reverse('informations:article-details',
                       kwargs={'slug': self.article.slug})


class ArticleNote(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('informations:article-details',
                       kwargs={'slug': self.article.slug})
