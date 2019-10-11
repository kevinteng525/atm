from django.db import models

# Create your models here.

# unit test or model test
class TestType(models.Model):
    name        = models.CharField(max_length=20, unique=True)
    desc = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_TestType"
        verbose_name = "Test Type"
        verbose_name_plural = verbose_name

class Tag(models.Model):
    name        = models.CharField(max_length=20, unique=True)
    desc        = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_Tag"

class TestCmd(models.Model):
    name        = models.CharField(max_length=50, unique=True)
    cmdline     = models.TextField(max_length=1000)
    block       = models.ForeignKey(to="ConfigModel.Block", on_delete=models.PROTECT, verbose_name="Block")
    project     = models.ForeignKey(to="ConfigModel.Project", on_delete=models.PROTECT, verbose_name="Project")
    testtype    = models.ForeignKey(to="TestType", on_delete=models.PROTECT, verbose_name="Test Type")
    priority    = models.SmallIntegerField(default=2, verbose_name="Priority")
    tag         = models.ManyToManyField(to="Tag", verbose_name="Tag")
    comment     = models.CharField(max_length=100, null=True, blank=True)
    is_delete   = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_TestCmd"
        verbose_name = "Test Command"
        verbose_name_plural = verbose_name

class TestCase(models.Model):
    name        = models.CharField(max_length=100, unique=True, verbose_name="Name")
    desc        = models.CharField(max_length=500, null=True, blank=True, verbose_name="Description")
    testcmd     = models.ForeignKey(to="TestCmd", on_delete=models.PROTECT, verbose_name="Commandline")
    precondition = models.TextField(max_length=1000, null=True, blank=True)
    config      = models.ForeignKey(to="ConfigModel.ConfigPlan", on_delete=models.PROTECT, null=True, blank=True)
    priority    = models.SmallIntegerField(default=2, verbose_name="Priority")
    tolerance   = models.CharField(max_length=20, default="0")
    timeout     = models.IntegerField(default=0)
    exectime    = models.FloatField(default=0, verbose_name="Execution Time")
    created     = models.DateField(auto_now_add=True)
    updated     = models.DateField(auto_now=True)
    is_delete   = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_TestCase"
        verbose_name = "Test Case"
        verbose_name_plural = verbose_name

class TestPlan(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    desc        = models.CharField(max_length=500, null=True, blank=True, verbose_name="Description")
    project     = models.ForeignKey(to="ConfigModel.Project", on_delete=models.PROTECT, verbose_name="Project")
    branch      = models.ForeignKey(to="ConfigModel.Branch", on_delete=models.PROTECT, verbose_name="Branch")
    dlframework = models.ForeignKey(to="ConfigModel.DLFramework", on_delete=models.PROTECT, verbose_name="DL Framework")
    runmode = models.ForeignKey(to="BuildModel.RunMode", on_delete=models.PROTECT, null=True, blank=True, verbose_name="Run Mode")
    testcase = models.ManyToManyField(to="TestCase",blank=True)
    config = models.ForeignKey(to="ConfigModel.ConfigPlan", on_delete=models.PROTECT, null=True, blank=True)
    #testcase    = models.ManyToManyField(to="TestCase", through='TestPlan_testcase')
    is_delete   = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_TestPlan"
        verbose_name = "Test Plan"
        verbose_name_plural = verbose_name

# class TestPlan_testcase(models.Model):
#     testplan    = models.ForeignKey(to="TestPlan", on_delete=models.PROTECT)
#     testcase    = models.ForeignKey(to="TestCase", on_delete=models.PROTECT)
#     is_enabled  = models.SmallIntegerField(default=1)
#
#     def __str__(self):
#         return "{0}-{1}".format(self.testplan, self.testcase)
#
#     class Meta:
#         db_table = "ATM_TestPlan_testcase"

class TestJob(models.Model):
    name        = models.CharField(max_length=50, unique=True)
    project     = models.ForeignKey(to="ConfigModel.Project", on_delete=models.PROTECT, null=True, blank=True, default=None, verbose_name="Project")
    buildplan = models.ForeignKey(to="BuildModel.BuildPlan", on_delete=models.PROTECT, null=True, blank=True, default=None)
    testplan    = models.ManyToManyField(to="TestPlan",blank=True)
    env         = models.ForeignKey(to="EnvModel.DockerImage", on_delete=models.PROTECT, null=True, blank=True, default=None, verbose_name="Environment")
    runMode     = models.ForeignKey(to="BuildModel.RunMode", on_delete=models.PROTECT, null=True, blank=True, default=None, verbose_name="Run Mode")
    parent      = models.ForeignKey(to='self', null=True, blank=True, default=None, on_delete=models.PROTECT, verbose_name="Parent Job")
    created     = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ATM_TestJob"
        verbose_name = "Test Job"
        verbose_name_plural = verbose_name
#
# class TestReport(models.Model):
#     task        = models.CharField(max_length=50)
#     project     = models.CharField(max_length=50)
#     testplan    = models.CharField(max_length=100)
#     testenv     = models.CharField(max_length=50)
#     testcase    = models.CharField(max_length=100)
#     result      = models.CharField(max_length=20)
#     failuretype = models.CharField(max_length=20)
#     testtime    = models.DateField(auto_now_add=True)
#
#
#     def __str__(self):
#         return "{0}_{1}".format(self.task + self.testtime)
#
#     class Meta:
#         db_table = "ATM_TestReport"