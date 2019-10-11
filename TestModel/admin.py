from django.contrib import admin, sites
from django.contrib.admin import SimpleListFilter
from TestModel.models import *
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.http import HttpResponse
import csv
import copy

# Register your models here.

class ExportCsvMixin(object):
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        response.charset = 'utf-8-sig'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = 'Export Selected as CSV'

class TagInline(admin.TabularInline):
    model = Tag

class TestCaseInline(admin.TabularInline):
    model = TestCase

class TestCmd_Admin(admin.ModelAdmin, ExportCsvMixin):
    actions = ['export_as_csv']
    search_fields = ('name', 'cmdline')
    inlines = [TestCaseInline, ]
    def tags(self, obj):
        return [a.name for a in obj.tag.all()]
    list_filter = ('block', 'project', 'priority', 'testtype')

    list_display = ('name', 'cmdline', 'block', 'project', 'priority', 'testtype', 'tags', 'comment')
    filter_horizontal = ('tag',)

    save_as = True

# class TestCaseInline(admin.TabularInline):
#     model = TestPlan_testcase

class TestPlanInline(admin.TabularInline):
    model = TestPlan.testcase.through
    fields = ['testplan']

    def testplan(self, instance):
        return instance.testplan.name

    testplan.short_description = 'testplan name'


def copy_testplan(modeladmin, request, queryset):
    for testplan in queryset:
        testplan_copy = copy.copy(testplan)  # (2) django copy object
        testplan_copy.id = None  # (3) set 'id' to None to create new object
        testplan_copy.name = testplan.name + "(cloned)"
        testplan_copy.save()  # initial save

        # (4) copy M2M relationship: testcase
        for testcase in testplan.testcase.all():
            testplan_copy.testcase.add(testcase)

        testplan_copy.save()  # (7) save the copy to the database for M2M relations

copy_testplan.short_description = "Clone Selected TestPlan"

class TestPlan_Admin(admin.ModelAdmin, ExportCsvMixin):
    # def cases(self, obj):
    #     return [a.name for a in obj.testcase.all()]

    # list_display = ('name', 'desc', 'project', 'branch', 'dlframework', 'runmode', 'cases', 'config')
    actions = [copy_testplan, 'export_as_csv']
    search_fields = ('name',)
    list_filter = ('project', 'branch', 'dlframework', 'runmode')
    list_display = ('name', 'desc', 'project', 'branch', 'dlframework', 'runmode', 'config')
    filter_horizontal = ('testcase',)
    save_as = True

class BlockFilter(SimpleListFilter):
    title = 'Block'
    parameter_name = 'block'


class AddTestPlanForm(ActionForm):
    testplans = forms.CharField(required=False)

def add_testplan(modeladmin, request, queryset):
    testplans_name = request.POST['testplans']
    testplans_name = testplans_name.replace(";", ",").replace(" ", ",")
    testplans_name_list = testplans_name.split(",")
    for testplan_name in testplans_name_list:
        testplans = TestPlan.objects.filter(name=testplan_name)
        if len(testplans) > 0:
            for testcase in queryset:
                testcase.testplan_set.add(testplans[0])
                testcase.save()

add_testplan.short_description = "Add Into TestPlans"

def remove_testplan(modeladmin, request, queryset):
    testplans_name = request.POST['testplans']
    testplans_name = testplans_name.replace(";", ",").replace(" ", ",")
    testplans_name_list = testplans_name.split(",")
    for testplan_name in testplans_name_list:
        testplans = TestPlan.objects.filter(name=testplan_name)
        if len(testplans) > 0:
            for testcase in queryset:
                testcase.testplan_set.remove(testplans[0])
                testcase.save()

remove_testplan.short_description = "Remove From TestPlans"


class TestCase_Admin(admin.ModelAdmin, ExportCsvMixin):
    action_form = AddTestPlanForm
    actions = [add_testplan, remove_testplan, 'export_as_csv']

    inlines = [TestPlanInline, ]
    def plans(self, obj):
        return [a.name for a in obj.testplan_set.all()]

    def configs(self, obj):
        ret = []
        if obj.config != None:
            for a in obj.config.config.all():
                ret.append(a)
        return ret

    def project(self, obj):
        return obj.testcmd.project

    def block(self, obj):
        return obj.testcmd.block

    def commandline(self, obj):
        return obj.testcmd.cmdline

    search_fields = ('name',)
    list_filter = ('testcmd__project', 'testcmd__block', 'priority')
    list_display = ('name', 'project', 'block', 'plans', 'commandline', 'priority', 'configs', 'desc', 'updated')

    save_as = True

class TestJob_Inline(admin.TabularInline):
    model = TestJob

class TestJob_Admin(admin.ModelAdmin, ExportCsvMixin):
    # inlines = [TestJob_Inline, ]
    # display be foreigned objects
    actions = ['export_as_csv']
    def sub_testjob(self, obj):
        return [a.name for a in obj.testjob_set.all()]

    def testplans(self, obj):
        return [a.name for a in obj.testplan.all()]

    search_fields = ('name',)
    list_filter = ('project', 'env', 'runMode')
    list_display = ('name', 'project', 'env', 'runMode', 'buildplan', 'testplans', 'sub_testjob')
    filter_horizontal = ('testplan',)

    save_as = True

admin.site.site_header = 'Alinpu Test Management'
admin.site.site_title = 'Login Alinpu Test Management Admin Site'
admin.site.index_title = 'Alinpu Test Management'

admin.site.register(TestPlan, TestPlan_Admin)

admin.site.register(TestCmd, TestCmd_Admin)

admin.site.register(TestCase, TestCase_Admin)

admin.site.register(TestJob, TestJob_Admin)

admin.site.register([TestType, Tag])