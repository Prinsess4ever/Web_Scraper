import requests
import os
import string
from bs4 import BeautifulSoup
from pathlib import Path


def Ik_weet_geen_naam(aantal_paginas, welk_article):
    lijst = []

    for i in range(1, aantal_paginas+1):
        print('for loop', i)
        donwload = requests.get(f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i}')
        download_html = BeautifulSoup(donwload.content, 'html.parser')
        articles = download_html.select('article')

        Path(rf"{os.getcwd()}\Page_{i}").mkdir(exist_ok=True)

        # loop over all the articles
        for article in articles:
            if article.select_one('.c-meta__item').text.strip() != welk_article:
                continue  # This is not the droid you are looking for!
            filename = ""

            # title veranderen in filename
            for word in article.select_one('.c-card__link').text.split():
                filename += f"{word.translate(str.maketrans('', '', string.punctuation))}_"
            print(' > ', filename)
            # achterste van link pakken
            link = article.select_one('.c-card__link')['href']
            print(link)
            # description downloaden
            page = requests.get(f'https://www.nature.com{link}')
            bsoup = BeautifulSoup(page.content, 'html.parser')
            result = bsoup.select_one('.c-article-body')

            # alles in file doen
            file = Path(rf"{os.getcwd()}\Page_{i}\{filename[:-1]}.txt")
            print(file)
            file.write_text(result.text, encoding='utf-8')

    return None


aantal_paginas = int(input())
welk_article = input()
a=Ik_weet_geen_naam(aantal_paginas, welk_article)
print("Saved all articles.")


