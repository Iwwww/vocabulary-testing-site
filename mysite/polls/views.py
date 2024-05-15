from typing import List
from random import uniform
import numpy as np

from django.db.models import F, Q, Func
from django.db.models.functions import Abs
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseBase
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.urls import reverse


from .models import Language, Word


def index(request):
    language_list = Language.objects.values_list("id", "language")
    select_language(request, language_list[0][0])  # language_list is not empty

    context = {"language_list": language_list, "current_page": "home"}
    return render(request, "polls/index.html", context)


def select_language(request, language_id):
    request.session["language_id"] = language_id


def language(request, language_id):
    language = get_object_or_404(Language, pk=language_id)
    words_list = Word.objects.filter(language=language_id)
    return render(
        request,
        "polls/language.html",
        {"language": language, "words_list": words_list, "current_page": "home"},
    )


def word(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    return render(request, "polls/word.html", {"word": word})


def testing(request):
    if "selected_words" in request.session and "word_tested_count" in request.session:
        request.session["word_tested_count"] += 1
        if request.session["word_tested_count"] >= len(
            request.session["selected_words"]
        ):
            del request.session["word_tested_count"]
            return HttpResponseRedirect(reverse("polls:result"))
    else:
        # Initilize "selected_words"
        words_count = 20
        selected_option = request.POST.get("test_length")
        if selected_option == "long":
            words_count = 80
        elif selected_option == "medium":
            words_count = 40

        request.session["selected_words"] = select_words(
            request.session["language_id"], words_count
        )

        request.session["word_tested_count"] = 0

    word_id = request.session["selected_words"][request.session["word_tested_count"]]

    word: Word = Word.objects.get(id=word_id)
    context = {"word": word}
    return render(request, "polls/testing.html", context)


def process_response(request):
    if request.method == "POST":
        response = request.POST.get("response")
        if response in ["know", "dont_know"]:
            # request.session["word_count_tested"] += 1
            if response == "know":
                pass
                # request.session["rank"] += request.session["last_rank"] + randint(
                #     0, 1000
                # )
            # elif response == "dont_know":
            #     if request.session["rank"] > 0:
            #         pass

        return HttpResponseRedirect(reverse("polls:testing"))


def result(request):
    # word_count_tested = request.session["word_count_tested"]
    # if word_count_tested <= 0:
    #     return HttpResponseRedirect(reverse("polls:testing"))
    # rank = request.session["rank"]
    # vocabular: int = int(rank / word_count_tested)

    # request.session["rank"] = 100
    # request.session["word_count_tested"] = 0

    vocabular: int = 0
    context = {"vocabular": vocabular}
    return render(request, "polls/result.html", context)


def about(request):
    context = {"current_page": "about"}
    return render(request, "polls/about.html", context)


def select_words(language_id: int, words_count: int) -> List[Word]:
    # Получаем все слова из базы данных
    all_words = Word.objects.filter(language_id=language_id, pos="s").values_list(
        "id", flat=True
    )

    # Генерация случайных смещений для выбора индексов
    random_offsets = [uniform(-50, 50) for _ in range(words_count)]

    # Равномерное распределение слов по сложности с учетом случайных смещений
    selected_indices = (
        np.linspace(0, len(all_words) - 1, words_count, dtype=int) + random_offsets
    )
    selected_indices = np.clip(selected_indices, 0, len(all_words) - 1).astype(int)

    # Выбор случайных слов из базы данных на основе случайных индексов
    selected_words = [all_words[int(index)] for index in selected_indices]

    return selected_words
