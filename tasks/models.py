from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todolist(models.Model):
    task = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    done = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, null=True, on_delete= models.CASCADE)

    def __str__(self):
        return self.task