from django.contrib import admin
from ConfigModel.models import *
from TestModel.admin import ExportCsvMixin
# Register your models here.

class ConfigDetail_Admin(admin.ModelAdmin):
    search_fields = ('name', 'content')
    list_filter = ('configtype',)
    list_display = ('name', 'desc', 'configtype', 'content')

    save_as = True

class ConfigPlan_Admin(admin.ModelAdmin, ExportCsvMixin):
    actions = ['export_as_csv']
    search_fields = ('name',)

    def configs(self, obj):
        return [a.name for a in obj.config.all()]

    list_display = ('name', 'desc', 'configs', 'is_delete')
    filter_horizontal = ('config',)

    save_as = True

admin.site.register(ConfigDetail, ConfigDetail_Admin)
admin.site.register(ConfigPlan, ConfigPlan_Admin)

admin.site.register([Project, Branch, DLFramework, OSType, Block, ConfigType])