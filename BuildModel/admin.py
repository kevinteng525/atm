from django.contrib import admin
from BuildModel.models import *
from TestModel.admin import ExportCsvMixin

# Register your models here.

class BuildDependency_Admin(admin.ModelAdmin):
    def dependprojectlist(self, obj):
        return [a.name for a in obj.dependprojects.all()]
    list_display = ('buildproject', 'dir', 'dependprojectlist')
    filter_horizontal = ('dependprojects',)

    save_as = True

class BuildDetail_Admin(admin.ModelAdmin):
    search_fields = ('name', 'options')
    list_filter = ('buildproject',)
    list_display = ('name', 'desc', 'buildproject', 'buildmode', 'buildtype', 'runmode', 'options', 'precondition')

    save_as = True

class BuildInfo_Admin(admin.ModelAdmin):
    def buildproject(self, obj):
        return obj.buildconfig.buildproject

    def buildmode(self, obj):
        return obj.buildconfig.buildmode

    def buildtype(self, obj):
        return obj.buildconfig.buildtype

    def runmode(self, obj):
        return obj.buildconfig.runmode

    def buildoptions(self, obj):
        return obj.buildconfig.options

    list_display = ('name', 'desc', 'buildproject', 'buildmode', 'buildtype', 'runmode', 'buildoptions')

class BuildPlan_Admin(admin.ModelAdmin, ExportCsvMixin):
    actions = ['export_as_csv']
    def buildconfigs(self, obj):
        return [a.name for a in obj.buildconfig.all()]

    list_filter = ('project', 'branch',)
    list_display = ('name', 'desc', 'project', 'branch', 'version', 'archived', 'buildconfigs')
    filter_horizontal = ('buildconfig',)

    save_as = True

admin.site.register(BuildPlan, BuildPlan_Admin)

admin.site.register(BuildDependency, BuildDependency_Admin)
admin.site.register(BuildDetail, BuildDetail_Admin)
admin.site.register([RunMode, BuildMode, BuildProject])