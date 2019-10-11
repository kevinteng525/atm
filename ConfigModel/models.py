from django.db import models

# Create your models here.
class Project(models.Model):
    name        = models.CharField(max_length=20, unique=True)
    desc        = models.CharField(max_length=100, null=True, blank=True)
    is_delete   = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_Project"

class OSType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    desc = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_OSType"

class Branch(models.Model):
    name        = models.CharField(max_length=20, unique=True)
    desc        = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_Branch"

class DLFramework(models.Model):
    name        = models.CharField(max_length=20, unique=True)
    desc        = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_DLFramework"

class Block(models.Model):
    name        = models.CharField(max_length=20, unique=True)
    desc        = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_Block"

class ConfigType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="Description")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_ConfigType"

class ConfigDetail(models.Model):
    name = models.CharField(max_length=20, unique=True)
    configtype = models.ForeignKey(to="ConfigType", on_delete=models.PROTECT, verbose_name="Config Type")
    desc = models.CharField(max_length=50, null=True, blank=True, verbose_name="Description")
    content = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_ConfigDetail"
        verbose_name = "Config Option"
        verbose_name_plural = verbose_name

class ConfigPlan(models.Model):
    name        = models.CharField(max_length=50, unique=True)
    desc        = models.CharField(max_length=100, null=True, blank=True, verbose_name="Description")
    config      = models.ManyToManyField(to="ConfigModel.ConfigDetail", blank=True)
    is_delete   = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_ConfigPlan"
        verbose_name = "Config Plan"
        verbose_name_plural = verbose_name