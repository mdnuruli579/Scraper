from django.db import models

# Create your models here.
class Theverge(models.Model):
    headline=models.CharField(max_length=1000,null=True,blank=True)
    link=models.CharField(max_length=1000,null=True,blank=True)
    author=models.CharField(max_length=500,null=True,blank=True)
    date=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.headline

