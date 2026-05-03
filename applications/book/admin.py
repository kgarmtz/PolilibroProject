from django.contrib import admin
# Local models
from .models import Unit, Chapter, Section, Resource

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    ordering = ('name',)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    ordering = ('name',)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter')
    ordering = ('name',)

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'file_type','chapter')
    ordering = ('chapter',)

# Register your models here.
admin.site.register(Unit, UnitAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Resource, ResourceAdmin)