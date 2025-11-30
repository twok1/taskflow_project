from django.contrib import admin

from .models import (
    Task,
    Project, 
    ProjectMembership,
    Tag,
    Comment,
    TaskProgress
)

admin.site.register(Task)
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(ProjectMembership)
admin.site.register(Comment)
admin.site.register(TaskProgress)