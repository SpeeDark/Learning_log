from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Домашяя страница приложения Learning Log."""
    # render - функция для построения шаблона сайта
    # request - запрос пользователя на URL.
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит одну тему и все её записи."""
    topic = get_list_or_404(Topic, id=topic_id)
    # Проверка того, что тема принадлежит пользователю.
    check_topic_owner(request, topic)
    # -date_added сортирует результаты в обратном порядке.
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправляются; создаётся пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST; обрабатываются данные.
        form = TopicForm(data=request.POST)
        # Проверяет, все ли поля заполнены.
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            # Записывает данные в базу.
            new_topic.save()
            # Перенаправяяем на страницу topics.
            return redirect('learning_logs:topics')
    
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Определяет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        # Данные не отправляются; создаётся пустая форма.
        form = EntryForm()
    else:
        # Отправлены данные POST; обрабатываются данные.
        form = EntryForm(data=request.POST)
        # Проверяет, все ли поля заполнены.
        if form.is_valid():
            # commit=False позволяет создать объект записи, не сохраняя пока в базу.
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            # Записывает данные в базу.
            new_entry.save()
            # Перенаправяяем на страницу topic/topic_id.
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        # instance=entry создаёт форму с заранее заполненной информацией о записи.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработка данных.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    # Вывести пустую или недействительную форму.
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_owner(request, topic):
    # Проверка принадлежности темы текущему пользователю.
    if topic.owner != request.user:
        raise Http404