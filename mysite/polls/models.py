from django.db import models
from django.db.models.fields.files import default_storage


class Language(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self):
        return str(self.language)


class Word(models.Model):
    lemma = models.CharField(max_length=50)
    pos = models.CharField(max_length=10)
    freq = models.FloatField()
    r = models.IntegerField()
    d = models.IntegerField()
    doc = models.IntegerField()
    difficulty = models.FloatField()
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.lemma)


class UserResponse(models.Model):
    user_session = models.CharField(max_length=255)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    response = models.BooleanField()  # True for "know", False for "don't know"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.user_session}, Word: {self.word}, Response: {self.response}"
