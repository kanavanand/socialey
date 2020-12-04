import re,string
import itertools
from textblob import TextBlob

def sentiment_analyzer_scores_text_blob(sentence):
    sentence = TextBlob(sentence)
    return sentence.sentiment.polarity


def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text


def strip_all_entities(text):
    text = remove_url(text)
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    if(len(words)>0):
        if words[0]=="rt" :
            return ' '.join(words[1:])
    return ' '.join(words)
def sentiment_final(x):
    if x<=-0.1:
        return "Negative"
    elif x>=0.1:
        return "Positive"
    else:
        return "Neutral"
    
def sentiment_final_int(x):
    if x<=-0.1:
        return -1
    elif x>=0.1:
        return 1
    else:
        return 0
    
def get_all_hashtags(sentence):
    return re.findall(r"#(\w+)", sentence)


def get_all_mentions(sentence):
    return re.findall(r"@(\w+)", sentence)

