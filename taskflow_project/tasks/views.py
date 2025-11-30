from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Project

@login_required
def project_list(request):
    """ выводим список проектов пользователя """
    projects = Project.objects.filter(member=request.user)
    return render(request, 'tasks/project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    """ информация о проекте """
    project = get_object_or_404(Project, id=project_id, members=request.user)
    tasks = project.tasks.all()
    return render(
        request,
        'tasks/project_detail.html',
        {
            'project': project,
            'tasks': tasks
        }
    )

@login_required
def task_detail(request, task_id):
    """ ифнормация о задаче """

    task = get_object_or_404(Task, id=task_id, project__members=request.user)
    comments = task.comments.all()
    progress_steps = task.progress_steps.all()

    return render(
        request, 'tasks/task_detail.html',
        {
            'task': task,
            'comments': comments,
            'progress_steps': progress_steps
        }

    )