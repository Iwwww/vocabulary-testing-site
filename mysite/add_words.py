#!/bin/env python3
from typing import List

from polls.models import Language, Word


def openFile(filename: str) -> List[List[str]]:
    data: List = []
    with open(filename, "r") as f:
        f.readline()
        for line in f.readlines():
            data.append(line.split())

    return data


def filterData(data: List[List[str]]) -> List[List[str]]:
    filtered_data = []
    for d in data:
        if d[1] == "s":
            filtered_data.append(d)

    return filtered_data


def add_words_from_dataframe(df):
    language, _ = Language.objects.get_or_create(id=1, defaults={"language": "Русский"})
    for index, row in df.iterrows():
        word = Word(
            lemma=row["Lemma"],
            pos=row["PoS"],
            freq=float(row["Freq(ipm)"]),
            r=int(row["R"]),
            d=int(row["D"]),
            doc=int(row["Doc"]),
            difficulty=float(row["Difficulty"]),
            language_id=language.id,  # Russian Language ID
        )
        word.save()
        print("Added:", row["Lemma"])


# data = openFile("freqrnc2011.csv")    # for prodaction
data = openFile("freqrnc2011-short.csv")  # for testing
# filtered_data = filterData(data)
# print("Words count:", len(filtered_data))

import numpy as np
import pandas as pd

# Создание DataFrame
df = pd.DataFrame(data, columns=["Lemma", "PoS", "Freq(ipm)", "R", "D", "Doc"])
print(df)

# Преобразование столбца Freq(ipm) в числовой тип
df["Freq(ipm)"] = pd.to_numeric(df["Freq(ipm)"])

# Фильтрация только существительных
# df = df[(df["PoS"] == "s")].copy()

# Рассчет сложности слова (чем реже слово, тем сложнее)
df["Difficulty"] = -np.log(df["Freq(ipm)"])

print(df)

# Сортируем слова по сложности
df = df.sort_values("Difficulty")

add_words_from_dataframe(df)

# pass

""" import random

# Количество слов в тесте
num_words = 20

# Генерация случайных смещений для выбора индексов
random_offsets = [random.uniform(-50, 50) for _ in range(num_words)]

# Равномерное распределение слов по сложности с учетом случайных смещений
selected_indices = (
    np.linspace(0, len(df) - 1, num_words, dtype=int) + random_offsets
)
selected_indices = np.clip(selected_indices, 0, len(df) - 1).astype(int)

# Выбор слов из DataFrame на основе случайных индексов
selected_words = df.iloc[selected_indices]
print(selected_words) """

""" 
import matplotlib.pyplot as plt

# Создание графика
plt.figure(figsize=(10, 6))
plt.plot(
    selected_words["Difficulty"],
    selected_words["Freq(ipm)"],
    marker="o",
    linestyle="-",
    color="b",
)

# Добавление заголовка и меток осей
plt.title("Сложность выбранных слов")
plt.ylabel("Индекс слова")
plt.xlabel("Сложность")
plt.yscale("log")

# Отображение графика
plt.tight_layout()
plt.show()
"""
