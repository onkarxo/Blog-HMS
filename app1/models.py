
# Create your models here.
# app1/models.py

from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=100, choices=[('Mental Health', 'Mental Health'), ('Heart Disease', 'Heart Disease'), ('Covid19', 'Covid19'), ('Immunization', 'Immunization')])
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=False)  # New field for draft status
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
