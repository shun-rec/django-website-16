from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    field1 = models.CharField(max_length=250, default="")
    field2 = models.CharField(max_length=250, default="")
    field3 = models.CharField(max_length=250, default="")
    field4 = models.CharField(max_length=250, default="")
    field6 = models.CharField(max_length=250, default="")
