from django.db import models

# Create your models here.

# cmodel / npu
class RunMode(models.Model):
    name = models.CharField(max_length=20, unique=True)
    desc = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_RunMode"

# rel / dbg
class BuildMode(models.Model):
    name = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_BuildMode"

class BuildProject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_BuildProject"

class BuildDependency(models.Model):
    buildproject = models.ForeignKey(to="BuildProject", on_delete=models.PROTECT, related_name="tobuild", unique=True, verbose_name="Project")
    dir = models.CharField(max_length=50, null=True, blank=True, verbose_name="Directory")
    dependprojects = models.ManyToManyField(to="BuildProject", blank=True, related_name="depends", verbose_name="Depends")

    def __str__(self):
        return self.buildproject.name

    class Meta:
        db_table = "ATM_BuildDependency"
        verbose_name = "Project Dependency"
        verbose_name_plural = verbose_name

class BuildDetail(models.Model):
    BUILDTYPES = (
        ('source', 'source'),
        ('package', 'package')
    )
    name = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="Description")
    buildproject = models.ForeignKey(to="BuildProject", on_delete=models.PROTECT, verbose_name="Project")
    buildmode = models.ForeignKey(to="BuildMode", on_delete=models.PROTECT, null=True, blank=True, verbose_name="Build Mode")
    buildtype = models.CharField(max_length=20, choices=BUILDTYPES, default="source", verbose_name="Build Type")
    runmode = models.ForeignKey(to="RunMode", on_delete=models.PROTECT, null=True, blank=True, verbose_name="Run Mode")
    precondition = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Pre-condition")
    options = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_BuildDetail"
        verbose_name = "Build Option"
        verbose_name_plural = verbose_name

class BuildPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="Description")
    version = models.CharField(max_length=20, default="latest")
    project = models.ForeignKey(to="ConfigModel.Project", on_delete=models.PROTECT)
    branch = models.ForeignKey(to="ConfigModel.Branch", on_delete=models.PROTECT)
    ostype = models.ForeignKey(to="ConfigModel.OSType", on_delete=models.PROTECT, verbose_name="OS Type")
    gcc_version = models.CharField(max_length=50, null=True, blank=True)
    archived = models.BooleanField(default=False)
    buildconfig = models.ManyToManyField(to="BuildDetail", verbose_name="Build Config")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_BuildPlan"
        verbose_name = "Build Plan"
        verbose_name_plural = verbose_name