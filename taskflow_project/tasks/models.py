from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    
    members = models.ManyToManyField(
        User, 
        through='ProjectMembership',
        related_name='projects',
        verbose_name="Участники"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Владелец'),
        ('editor', 'Редактор'), 
        ('viewer', 'Наблюдатель'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'project']


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Цвет")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Метка"
        verbose_name_plural = "Метки"


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'К выполнению'),
        ('in_progress', 'В процессе'),
        ('done', 'Выполнено'),
        ('blocked', 'Отложено'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Обычный'),
        ('high', 'Высокий'),
        ('critical', 'Критический'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        verbose_name="Проект"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Метки")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='todo',
        verbose_name="Статус"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES, 
        default='medium',
        verbose_name="Приоритет"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-created_at']


class TaskProgress(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='progress_steps',
        verbose_name="Задача"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Автор действия"
    )
    description = models.TextField(verbose_name="Выполненная работа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выполнения")
    
    def __str__(self):
        return f"Прогресс по {self.task.title} - {self.author.username}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Шаг выполнения"
        verbose_name_plural = "Шаги выполнения"


class Comment(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="Задача"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Комментарий от {self.author} к {self.task}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"