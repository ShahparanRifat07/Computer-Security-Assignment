from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
from auditlog.registry import auditlog
# Create your models here.

class CustomUser(models.Model):
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.username

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Code(models.Model):
    number = models.CharField(max_length=6, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        number_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        code_item = []
        for i in range(6):
            num = random.choice(number_list)
            code_item.append(num)
        code_string = ""
        for i in range(len(code_item)):
            code_string = code_string + str(code_item[i])
        self.number = code_string
        super().save(*args, **kwargs)
    

auditlog.register(Blog)
