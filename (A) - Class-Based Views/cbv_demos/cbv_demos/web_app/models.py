from django.db import models


class ArticleModel(models.Model):
    title = models.CharField(max_length=50,
                             null=False)

    content = models.TextField(null=False)
