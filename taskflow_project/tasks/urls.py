from django.urls import path
from . import views

app_name = 'tasks'

url_patterns = [
    path('', views.project_list, name='project_list')
    path('project/<int:project_id>', views.project_detail, name='project_detail')
    path('task/<int:task_id', view.task_detail, name='task_detail')
]