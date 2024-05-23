from django.core.exceptions import ValidationError
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


class AssessmentParameters(models.Model):
    max_known_words = models.IntegerField(default=105000)  # L
    rate_change_coefficient = models.FloatField(default=0.25)  # k
    average_theta = models.FloatField(default=-1.5)  # theta_0

    def __str__(self):
        return f"Max known words: {self.max_known_words}, rate change coefficient: {self.rate_change_coefficient}, average theta: {self.average_theta}"

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("There can be only one AssessmentParameters instance")
        return super(AssessmentParameters, self).save(*args, **kwargs)


class UserResponse(models.Model):
    user_session = models.CharField(max_length=255)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    response = models.BooleanField()  # True for "know", False for "don't know"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.user_session}, Word: {self.word}, Response: {self.response}"
