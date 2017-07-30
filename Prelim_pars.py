import os
import json
import string
import requests
from flask import Flask, Response
app = Flask(__name__)

@app.route('/parse/<string:file>')
def quizzer_pars(file):
    reference = set(string.punctuation)
    article = open(str(file), 'r')
    long_art_string= article.read()
    no_newline = long_art_string.replace("\n", " ")
    if "!" in no_newline:
        no_sent_punct = no_newline.split("!")
        for elem in no_sent_punct:
            if "." in elem:
                sam = elem.split(".")
                no_sent_punct.remove(elem)
                no_sent_punct.append(sam)
    else:
        no_sent_punct = no_newline.split(".")
    ultimatum ={}
    for phrase in no_sent_punct:
        if "?" in phrase:
            medium = phrase.slice("?")
            pos_ques = medium[0]
            medium = medium.remove(pos_ques)
            ultimatum[pos_ques] = str(medium)
        else:
            ultimatum[phrase] = 'determination'
    return str(ultimatum)

@app.route('/ping/<article_name>')
def ping(article_name):
    api_url = 'https://en.wikipedia.org/w/api.php?action=parse&format=json&page=' + article_name + '&redirects=&prop=wikitext'
    return requests.get(api_url).content

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)