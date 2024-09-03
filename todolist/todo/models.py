from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    taskname = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=50)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE) 