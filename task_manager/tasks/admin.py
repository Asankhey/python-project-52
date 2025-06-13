from django.contrib import admin
from task_manager.tasks.models import Task, TaskRelationLabel


class TaskRelationLabelInline(admin.TabularInline):
    model = TaskRelationLabel
    extra = 1
    verbose_name = 'Метка'
    verbose_name_plural = 'Метки'


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'author', 'executor', 'created_at')
    inlines = [TaskRelationLabelInline]


admin.site.register(Task, TaskAdmin)
