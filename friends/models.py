from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)
    book = models.CharField(max_length=50)
    is_valid = models.BooleanField()

    def __str__(self):
        return f"{self.name}"