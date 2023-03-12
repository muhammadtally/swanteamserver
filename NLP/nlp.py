import re
import hebrew_tokenizer as ht
from collections import Counter
from pathlib import Path


def get_stopwords():
    stop_words = open((Path(__file__).parent / 'stop_words.txt'), encoding="utf8").read()
    stop_words = clean_text(stop_words)
    stop_words_list = tokenize_hebrew(stop_words)
    return stop_words_list

def clean_text(text):
    text=text.replace('\n', ' ').replace('\r', ' ')
    pattern= re.compile(r'[^א-ת\s.",!?a-zA-Z]')
    alnum_text =pattern.sub(' ', text)
    while(alnum_text.find('  ')>-1):
            alnum_text=alnum_text.replace('  ', ' ')
    return alnum_text


def tokenize_hebrew(text):
    text_tokens = ht.tokenize(text)
    text_token = []
    for grp, token, token_num, (start_index, end_index) in text_tokens:
        if(grp == "HEBREW" or grp == "HOUR" or grp == "DATE"):
            text_token.append(token)
    return text_token

def remove_stop_words(text_tokens):
    for token in list(text_tokens):
        if token in get_stopwords():
            text_tokens.remove(token)
    return text_tokens

def procces_text(text):
    txt = clean_text(text)
    text_token = tokenize_hebrew(txt)
    text_token_without = remove_stop_words(text_token)
    return text_token_without



