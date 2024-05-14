from django.db import models
from django.db.models.fields.files import default_storage


class Language(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self):
        return str(self.language)


class Word(models.Model):
    word = models.CharField(max_length=50)
    rank = models.IntegerField()
    meaning = models.CharField(max_length=300)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    MAX_RANK = 300_000

    def __str__(self):
        return str(self.word)
