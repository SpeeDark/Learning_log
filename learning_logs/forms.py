from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        # Создаётся на базе модели Topic.
        model = Topic
        # На ней размещается только текст.
        fields = ['text']
        # Не генерировать подпись для текстового поля.
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        # Создаётся на базе модели Entry.
        model = Entry
        # На ней размещается только текст.
        fields = ['text']
        # Не генерировать подпись для текстового поля.
        labels = {'text': 'Entry:'}
        # Текстовая область с максимальной длинной в 80 симв.
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}