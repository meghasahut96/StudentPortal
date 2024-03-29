from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  title=models.CharField(max_length=200)
  desc=models.TextField()
  def __str__(self):
    return self.title
  class Meta:
    verbose_name = 'Notes'
    verbose_name_plural = 'Notes'

class Homework(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  subject=models.CharField(max_length=50)
  title=models.CharField(max_length=100)
  desc=models.TextField()
  due=models.DateTimeField()
  is_finished=models.BooleanField(default=False)  


  def __str__(self):
      return self.subject    
# Create your models here.

class Todo(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  title=models.CharField(max_length=100)
  is_finished=models.BooleanField(default=False)

  def __str__(self):
      return self.title
  