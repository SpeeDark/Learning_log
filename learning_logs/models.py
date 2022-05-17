from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
	"""Тема, которую изучает пользователь."""
	# CharField нужно для хранения небольших данных.(заглавия, имена, названия)
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		"""Возвращает стоковое представление модели."""
		return self.text

class Entry(models.Model):
	"""Информация, изученная пользователем по теме."""
	# ForeignKey содержит ссылку на другую запись в базе данных.
	# Аргумент on_delete=models.CASCADE сообщает, что при удалении темы все записи с ней должны быть удалены.
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	# TextField - ячейка хранения текста любой длинны.
	text = models.TextField()
	# date_added отображает записи в порядке их создания и снабжает запись временной меткой.
	date_added = models.DateTimeField(auto_now_add=True)

	# Meta вкладывается в класс Entry и позволяет хранить название Entry во мн.числе.
	# Без Meta django использует Entrys(неправильная форма).
	class Meta:
		verbose_name_plural = 'entries'
	
	def __str__(self):
		"""Возвращает стоковое преставление модели."""
		return f"{self.text[:50]}..."