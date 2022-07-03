import bs4.element
import spacy
import os
import ndjson
import json
import random
import time
from source_parser import NapoliTodayParser, match_place_type
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import re


# article = NapoliTodayParser("https://www.napolitoday.it/cronaca/condannati-minorenni-rider-rapinato.html")
# article = article.get_article()


# with open("napolitoday.json", "r") as f:
#     json = json.load(f)
#     print(json["aggregations"][0]["values"][0]["key"])
#     set_luoghi = set()
#     for key in json["aggregations"][0]["values"]:
#         set_luoghi.add(key["key"].split()[0])
#         # print(key["key"].split()[0])

nlp = spacy.load("it_core_news_lg")

# rapine = []
# for f in tqdm(os.listdir("data")):
#     with open(f"data/{f}", "r", encoding="UTF8") as file:
#         txt = file.read()
#         doc = nlp(txt)
#         ents = doc.ents
#         for e in ents:
#             if e.label_ == "LOC":
#                 if "/" not in e.text:
#                     if match_place_type(e.text):
#                         # print(f"{e.text} - {f} - {doc[e.start - 5:e.end + 5]}")
#                         e_text = e.text.replace('\n', '')
#                         # print(f"{e_text} - {doc[:1]}")
#                         bundle = {"loc": e_text, "date": str(doc[:1])}
#                         rapine.append(bundle)
#                         # print(bundle)
# print(len(rapine))



rapine = []
with open("data/links.txt", "r", encoding="UTF8") as f:
    for url in tqdm(f.readlines()):
        article = NapoliTodayParser(url.strip())
        bundle = article.get_rapina_bundle(nlp)
        if bundle:
            rapine.append(bundle)
print(rapine)
with open("json/bulk.ndjson", "w", encoding="UTF8") as f:
    writer = ndjson.writer(f, ensure_ascii=False)

    for r in rapine:
        writer.writerow({"create": {}})
        writer.writerow(r)
