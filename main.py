import bs4.element
import spacy
import os
import ndjson
import random
import time
from source_parser import NapoliTodayParser
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


nlp = spacy.load("it_core_news_lg")
json_file = open("json/bulk.json", "w", encoding="UTF8")

rapine = []
# article = NapoliTodayParser("https://www.napolitoday.it/cronaca/condannati-minorenni-rider-rapinato.html")
# article = article.get_article()


# with open("data/links.txt", "r", encoding="UTF8") as f:
#     for url in tqdm(f.readlines()):
#         # print(url.strip())
#         article= NapoliTodayParser(url.strip())
#         art = article.dump_article()


#     doc = nlp(txt)
#     ents = doc.ents
#
#     for e in ents:
#         if e.label_ == "LOC":
#             if "via" in e.text:
#                 rapina = {}
#                 rapina["loc"] = e.text
#                 rapina["date"] = "2021/01/01"
#                 rapine.append(rapina)

# print(rapine[0])
# json.dump(rapine, json_file, indent= 2)

# Writing items to a ndjson file
# with open("json/bulk.ndjson", "w", encoding="UTF8") as f:
#     writer = ndjson.writer(f, ensure_ascii=False)
#
#     for r in rapine:
#         writer.writerow({"create": {}})
#         writer.writerow(r)