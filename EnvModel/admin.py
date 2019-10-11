from django.contrib import admin
from EnvModel.models import *

# Register your models here.
class DockerImage_Admin(admin.ModelAdmin):
    list_filter = ('name', 'repo', 'tag')
    list_display = ('name', 'repo', 'tag')

    save_as = True


admin.site.register(DockerImage, DockerImage_Admin)