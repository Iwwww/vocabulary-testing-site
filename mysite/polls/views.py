from typing import List
from random import randint

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
    # if "rank" not in request.session:
    #     request.session["rank"] = 100
    #
    # if "word_count_tested" not in request.session:
    #     request.session["word_count_tested"] = 0
    #
    # if request.session["word_count_tested"] >= 20:
    #     return HttpResponseRedirect(reverse("polls:result"))

    # target_rank = request.session["rank"]
    # word_count_tested: int = request.session["word_count_tested"]
    # tolerance = 50 * word_count_tested * 2**word_count_tested
    # tolerance = 500
    # words_query = Word.objects.filter(
    #     Q(rank__gte=target_rank) & Q(rank__lte=target_rank + tolerance)
    # )
    # word_query = (
    #     Word.objects.filter(rank__isnull=False)
    #     .annotate(diff=Abs(F("rank") - target_rank))
    #     .order_by("diff")
    # )
    # word: str = word_query.first()
    # print("WORD:", word)
    # request.session["last_rank"] = word.rank

    word: str = "hello"
    context = {"word": word}
    return render(request, "polls/testing.html", context)


def process_response(request):
    if request.method == "POST":
        response = request.POST.get("response")
        if response in ["know", "dont_know"]:
            request.session["word_count_tested"] += 1
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
