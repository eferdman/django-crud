from django.db import models

# Create your models here.
from django.db import models

class Person(models.Model):
        last_name = models.CharField(max_length=200)
        first_name = models.CharField(max_length=200)

        def __str__(self):
        	return self.first_name + " " + self.last_name