
from bs4 import BeautifulSoup
import json

with open("index.html", "r") as file:
    contents = file.read()
    b = {}
    all_doc = BeautifulSoup(contents, 'lxml')
    for i in all_doc.recursiveChildGenerator():

        if i.name == 'p':
            b.update({'абзац': i.text})
        elif i.name == 'figure':
            b.update({'jpg': i})


        print(b)

