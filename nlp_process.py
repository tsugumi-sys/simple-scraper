import pandas as pd
import numpy as np
from scraper import scrape_note, scrape_ameba_blog
import spacy


def make_text_data(search_query=None):
    if search_query == None:
        search_query = ["行政書士", "家族信託", "相続"]
    content_df = pd.concat([scrape_ameba_blog(search_query), scrape_note(search_query)])
    text = ''
    for i in content_df["CONTENT"]:
        text += i
    with open('test.txt', 'w') as f:
        f.write(text)
    return {"status text": "OK"}

def word_count():
    # Load Data
    with open('test.txt', 'r') as f:
        text = f.read()
    
    # NLP Process
    nlp = spacy.load("ja_core_news_sm")
    doc = nlp(text)

    # Word Count of Noun
    word_count = {}
    for token in doc:
        part_of_speech = token.pos_
        if part_of_speech == 'NOUN' and token.is_stop == False:
            word_lemma = token.lemma_
            current_count = word_count.get(word_lemma, 0)
            current_count += 1
            word_count[word_lemma] = current_count

    return_word_count = {}
    for key, val in word_count.items():
        if val > 10:
            return_word_count[key] = val
    print(return_word_count)

    return return_word_count


# Parameter
# ==================
# a, b: word vector comes from spacy vector object
def cosine_similarity(a, b):
    return a.dot(b)/np.sqrt(a.dot(a) * b.dot(b))

# Parameter
# ==================
# search_query: list
# kwds_query: list
def nlp_process(search_query=None, kwds_query=None):
    # Set keyword parapeter
    if kwds_query:
        keyword_query = kwds_query
    else:
        keyword_query = ["行政書士", "家族信託", "相続"]
    print('-'*40, keyword_query, '-'*40)
    keyword_text = ''
    for kwd in  keyword_query:
        keyword_text += kwd


    # Load Data
    content_df = pd.concat([scrape_ameba_blog(search_query), scrape_note(search_query)])

    # NLP Process
    nlp = spacy.load("ja_core_news_sm")
    scores = []
    kwds_vec = nlp(keyword_text).vector

    for content in content_df["CONTENT"]:
        content_vec = nlp(content).vector
        score = cosine_similarity(kwds_vec, content_vec)
        scores.append(score)

    content_df["SCORE"] = scores
    content_df = content_df.sort_values(by='SCORE', ascending=False)

    return {
        'keyword': keyword_query,
        'url': content_df["URL"][:10].values.tolist(),
        'content': content_df["CONTENT"][:10].apply(lambda x: x[:250] if len(x) > 250 else x).values.tolist()
    }

if __name__ == '__main__':
    word_count()