from django.db import models

# Create your models here.

class News_model(models.Model):
    title=models.CharField(max_length=1000,null=True)
    date=models.CharField(max_length=100,null=True)
    publised=models.CharField(max_length=100,null=True)
    url=models.CharField(max_length=500,null=True)
    keyword=models.CharField(max_length=500,null=True)

class Article(models.Model):
    news=models.ForeignKey(News_model,on_delete=models.CASCADE)
    article=models.TextField()
    isScrap=models.BooleanField(default=False)
