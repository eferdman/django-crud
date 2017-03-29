from django.db import models

# Create your models here.
class UserTables(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    table_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name + " " + self.table_name

class Columns(models.Model):
    id = models.BigAutoField(primary_key=True)
    table = models.ForeignKey(UserTables)
    column_name = models.CharField(max_length=100)
    column_type = models.CharField(max_length=100)
    column_sequence = models.IntegerField()

    def __str__(self):
        return self.column_name + ", " + self.column_type