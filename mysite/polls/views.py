from typing import List

from django.http import Http404, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse


from .models import Language, Word


def index(request):
    language_list= Language.objects.values_list('id', 'language')
    select_language(request, language_list[0][0])  # language_list is not empty

    context = {"language_list": language_list}
    return render(request, "polls/index.html", context)


def select_language(request, language_id):
    request.session["language_id"] = language_id


def language(request, language_id):
    language = get_object_or_404(Language, pk=language_id)
    words_list = Word.objects.filter(language=language_id)
    return render(
        request, "polls/language.html", {"language": language, "words_list": words_list}
    )


def word(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    return render(request, "polls/word.html", {"word": word})


def meaning(request, word_id):
    response = "You're looking at the meaning of word %s."
    return HttpResponse(response % word_id)


def testing(request):
    if "rank" not in request.session:
        request.session["rank"] = 0

    # word = Word.objects.filter(rank=request.session["rank"]).first()
    word = Word.objects.order_by("?").first()
    request.session["last_rank"] = word.rank

    context = {"word": word}
    return render(request, "polls/testing.html", context)


def process_response(request):
    if request.method == "POST":
        response = request.POST.get("response")
        if response in ["know", "dont_know"]:
            if response == "know":
                request.session["rank"] += request.session["last_rank"]
            elif response == "dont_know":
                if request.session["rank"] > 0:
                    pass
                    # request.session["rank"] -= 1

        return HttpResponseRedirect(reverse("polls:testing"))
