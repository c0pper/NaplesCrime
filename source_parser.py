from bs4 import BeautifulSoup
import requests
import re
import locale
from datetime import datetime
from tqdm import tqdm
locale.setlocale(locale.LC_TIME, "it_IT")
import spacy
import ndjson


def match_place_type(found_loc):
    # places_types = {'contrada',
    #                 'corso',
    #                 'viale',
    #                 'via',
    #                 'largo',
    #                 'piazza',
    #                 'strada',
    #                 'vico',
    #                 'vicolo',
    #                 'salita',
    #                 'piazzetta',
    #                 'piazzale',
    #                 'napoli centrale',
    #                 'capodimonte'}
    # result = False
    # for x in places_types:
    #     if x in found_loc.lower():
    #         return True

    pattern = 'contrada|corso|viale|via|largo|piazza|strada|vico|vicolo|salita|piazzetta|piazzale|napoli centrale|capodimonte'
    result = re.search(pattern, found_loc, re.IGNORECASE)
    # print(result)
    if result:
        return True

# todo def not_match_type():
#   autostrada, circumvesuviana, polstrada


class Parser:
    def __init__(self, url):
        self.url = url
        req = requests.get(self.url)
        self.soup = BeautifulSoup(req.content, 'html.parser')

    def join_paragraphs(self, soup_spoon):
        soup_spoon = (" ".join(soup_spoon) if len(soup_spoon) > 1 else soup_spoon[0].text)
        soup_spoon = re.sub(r'\n+', '', soup_spoon).strip()
        soup_spoon = soup_spoon.replace(" ", " ")

        return soup_spoon


class NapoliTodayParser(Parser):
    title_class = 'l-entry__title'
    summary_class = 'l-entry__summary'
    text_class = 'c-entry'
    date_class = 'u-label-08'


    def __init__(self, url):
        super().__init__(url)

    def get_article(self, print_text=False):
        print(self.url)
        if self.soup.select("body > div.o-wrapper.o-bg-base > main > div.o-container > article > section.u-mb-medium\@xl > header > h1"):
            title = self.soup.select("body > div.o-wrapper.o-bg-base > main > div.o-container > article > section.u-mb-medium\@xl > header > h1")[0].text
            if print_text: print(title)
            summary = self.soup.select("body > div.o-wrapper.o-bg-base > main > div.o-container > article > section.u-mb-medium\@xl > header > p")[0].text
            if print_text: print(summary)
            text = self.soup.select("body > div.o-wrapper.o-bg-base > main > div.o-container > article > section.u-mb-medium\@xl > section.l-entry__body > div")[0].find_all("p")
            text = "\n".join([t.text for t in text])
            if print_text: print(text)
            date = self.soup.select("body > div.o-wrapper.o-bg-base > main > div.o-container > article > section.u-mb-medium\@xl > section.l-entry__byline.u-flex > div.u-flex.u-column\@xl.u-items-center.u-items-start\@xl.u-mb-small\@xl > div:nth-child(2) > span.u-label-08.u-color-light.u-block")
            if date:
                date = datetime.strptime(self.join_paragraphs(date), "%d %B %Y %H:%M").strftime("%Y/%m/%d") #07 aprile 2022 10:50
            else:
                date = self.soup.select("body > div.o-wrapper.o-bg-base > main > div.o-container > article > section.l-entry__related.u-mb-medium > section > div.u-flex.u-column\@xl.u-items-center.u-items-start\@xl.u-mb-small\@xl > div:nth-child(2) > span.u-label-08.u-color-secondary.u-block")
                date = datetime.strptime(self.join_paragraphs(date), "%d %B %Y %H:%M").strftime("%Y/%m/%d")  # 07 aprile 2022 10:50
            if print_text: print(date)
            body = title + " \n" + summary + " \n" + text
            article = {"date": date, "body": body, "title": title, "summary": summary, "text": text, "url": self.url}

            return article

    def dump_article(self):
        article = self.get_article()
        if article:
            fname = " ".join(article["title"].split()[:6]).replace(" ", "_")
            fname = re.sub(r'[^\w\s]', '', fname)
            with open(f"data/{fname}.txt", "w", encoding="UTF8") as f:
                f.write("\n".join([v for k, v in article.items()]))

    def get_all_art_links(self):
        links = []
        for i in tqdm(range(1, 41)):
            page_url = f"https://www.napolitoday.it/tag/rapine/pag/{i}/"
            req = requests.get(page_url)
            soup = BeautifulSoup(req.content, 'html.parser')
            articles = soup.find_all('article')
            # print(len(articles))
            for art in articles:
                if art.header.contents[3].has_attr('href'):
                    links.append("https://www.napolitoday.it" + art.header.contents[3]["href"])
                    # print("https://www.napolitoday.it" + art.header.contents[3]["href"])

        links = set(links)
        print(len(links))
        with open("data/NTlinks.txt", "w", encoding="UTF8") as f:
            for l in links:
                f.write(l + "\n")

    def get_rapina_bundle(self, nlp):
        article = self.get_article()
        if article:
            body = article["body"]
            doc = nlp(body)
            ents = doc.ents
            for e in ents:
                if e.label_ == "LOC":
                    if "/" not in e.text:
                        if match_place_type(e.text):
                            # print(f"{e.text} - {f} - {doc[e.start - 5:e.end + 5]}")
                            e_text = e.text.replace('\n', '')
                            # print(f"{e_text} - {doc[:1]}")
                            bundle = {"loc": e_text, "date": article["date"], "url": article["url"]}
                            print(bundle)
                            return bundle
                else:
                    pass


    def __str__(self):
        article = self.get_article()
        return "\n".join([v for k, v in article.items()])
