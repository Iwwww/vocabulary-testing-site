from typing import List
from random import uniform
import numpy as np
from scipy.optimize import minimize

from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Language, Word


def index(request):
    if request.session in ["word_tested_count"]:
        del request.session["word_tested_count"]
    if request.session in ["selected_words"]:
        del request.session["selected_words"]
    if request.session in ["responses"]:
        del request.session["responses"]

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
        if request.session["word_tested_count"] >= len(
            request.session["selected_words"]
        ):
            del request.session["word_tested_count"]
            return HttpResponseRedirect(reverse("polls:result"))
    else:
        # Initilize
        words_count = 20
        selected_option = request.POST.get("test_length")
        if selected_option == "long":
            words_count = 80
        elif selected_option == "medium":
            words_count = 40

        request.session["selected_words"] = select_words(
            request.session["language_id"], words_count
        )
        request.session["responses"] = []
        request.session["word_tested_count"] = 0

    word_id = request.session["selected_words"][request.session["word_tested_count"]]

    word: Word = Word.objects.get(id=word_id)
    context = {"word": word}
    return render(request, "polls/testing.html", context)


def process_response(request):
    if request.method == "POST":
        response = request.POST.get("response")
        if response in ["know", "dont_know"]:
            try:
                request.session["word_tested_count"] += 1
                if response == "know":
                    request.session["responses"].append(1)
                else:
                    request.session["responses"].append(0)
            except:
                pass

    return HttpResponseRedirect(reverse("polls:testing"))


def result(request):
    theta_hat: float = assessment_of_skills(
        request.session["selected_words"], request.session["responses"]
    )
    # Оценка уровня навыков пользователя (θ), полученная ранее
    estimated_vocab_size = estimate_vocab_size(theta_hat)

    print(f"Оценка словарного запаса пользователя: {estimated_vocab_size:.2f} слов")
    vocabular: int = int(round(estimated_vocab_size, -3))
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


def logistic_func(theta, b):
    """
    Logistic function used in 1PL IRT model.

    Parameters:
    theta (float or numpy.ndarray): Skill level of the user (scalar or array).
    b (numpy.ndarray): Difficulty levels of the words (array).

    Returns:
    numpy.ndarray: Probabilities of knowing each word.
    """
    return 1 / (1 + np.exp(-(theta - b)))


def neg_log_likelihood(theta, responses, b):
    """
    Negative log-likelihood function for 1PL IRT model.

    Parameters:
    theta (float): Skill level of the user.
    responses (numpy.ndarray): User's responses (1 if known, 0 if not known).
    b (numpy.ndarray): Difficulty levels of the words.

    Returns:
    float: Negative log-likelihood.
    """
    responses_array = np.array(responses)
    probabilities = logistic_func(theta, b)
    likelihoods = responses_array * np.log(probabilities) + (
        1 - responses_array
    ) * np.log(1 - probabilities)
    return -np.sum(likelihoods)


def assessment_of_skills(selected_word_ids, responses) -> float:
    words = Word.objects.filter(pk__in=selected_word_ids)
    word_dict = {word.id: word for word in words}
    selected_words = [word_dict[word_id] for word_id in selected_word_ids]

    # Оценка уровня навыков пользователя (θ)
    initial_theta = 0  # начальное значение θ
    difficulties = [word.difficulty for word in selected_words]

    result = minimize(
        neg_log_likelihood, initial_theta, args=(responses, difficulties), method="BFGS"
    )
    theta_hat = result.x[0]

    print(f"Оценка уровня навыков пользователя: {theta_hat}")
    return theta_hat


def estimate_vocab_size(theta):
    L = 105000  # Максимальное количество известных слов
    k = 0.3  # Коэффициент скорости изменения
    theta_0 = -4  # Среднее значение theta

    # Логистическая функция для оценки словарного запаса
    vocab_size = L / (1 + np.exp(-k * (theta - theta_0)))
    return vocab_size
