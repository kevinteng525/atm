from django.db import models

# Create your models here.

class DockerImage(models.Model):
    name = models.CharField(max_length=50, unique=True)
    repo = models.CharField(max_length=100, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    dockerfile = models.TextField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_DockerImage"