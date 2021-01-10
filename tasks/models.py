from django.db import models

# Create your models here.
class Todolist(models.Model):
    task = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.task