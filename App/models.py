from django.db import models

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    width = models.IntegerField()
    height = models.IntegerField()

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Annotation(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    bbox = models.JSONField()
    area = models.IntegerField()
    iscrowd = models.BooleanField(default=False)
