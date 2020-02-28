import random
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

file_path = 'text_emotion.csv'
content = 'content'
user = 'author'
sen = 'sentiment'

nonTnonS = 'nonTnonS_text_emotion.csv'
TnonS = 'red_bal_TnonS_text_emotion.csv'
nonTPS = 'nonTPS_text_emotion.csv'
TPS = 'red_bal_TPS_text_emotion.csv'
nonTLS = 'nonTLS_text_emotion.csv'
TLS = 'red_bal_TLS_text_emotion.csv'

mergeTLS = 'merge_TLS_text_emotion.csv'
mergeTPS = 'merge_TPS_text_emotion.csv'

test1 = 'test1.csv'


def remove_symbols():
    df[content] = df[content].apply(lambda x: x.replace("$", ''))
    df[content] = df[content].apply(lambda x: x.replace("%", ''))
    df[content] = df[content].apply(lambda x: x.replace("&", ''))
    df[content] = df[content].apply(lambda x: x.replace("(", ''))
    df[content] = df[content].apply(lambda x: x.replace(")", ''))
    df[content] = df[content].apply(lambda x: x.replace("+", ''))
    df[content] = df[content].apply(lambda x: x.replace(",", ''))
    df[content] = df[content].apply(lambda x: x.replace("-", ''))
    df[content] = df[content].apply(lambda x: x.replace(".", ''))
    df[content] = df[content].apply(lambda x: x.replace("/", ''))
    df[content] = df[content].apply(lambda x: x.replace(":", ''))
    df[content] = df[content].apply(lambda x: x.replace(";", ''))
    df[content] = df[content].apply(lambda x: x.replace("<", ''))
    df[content] = df[content].apply(lambda x: x.replace(">", ''))
    df[content] = df[content].apply(lambda x: x.replace("=", ''))
    df[content] = df[content].apply(lambda x: x.replace("?", ''))
    df[content] = df[content].apply(lambda x: x.replace("@", ''))
    df[content] = df[content].apply(lambda x: x.replace("[", ''))
    df[content] = df[content].apply(lambda x: x.replace("]", ''))
    df[content] = df[content].apply(lambda x: x.replace("^", ''))
    df[content] = df[content].apply(lambda x: x.replace("_", ''))
    df[content] = df[content].apply(lambda x: x.replace("`", ''))
    df[content] = df[content].apply(lambda x: x.replace("{", ''))
    df[content] = df[content].apply(lambda x: x.replace("}", ''))
    df[content] = df[content].apply(lambda x: x.replace("~", ''))
    df[content] = df[content].apply(lambda x: x.replace("|", ''))
    df[content] = df[content].apply(lambda x: x.replace("£", ''))
    df[content] = df[content].apply(lambda x: x.replace("€", ''))

    df[content] = df[content].apply(lambda x: x.replace("'", ''))
    df[content] = df[content].apply(lambda x: x.replace('"', ''))
    df[content] = df[content].apply(lambda x: x.replace("\\", ""))
    df[content] = df[content].apply(lambda x: x.replace("\t", ""))


def lower():
    df[content] = df[content].apply(lambda x: x.lower())


def remove_urls():
    df[content] = df[content].apply(lambda x: ' '.join(
        word for word in x.split(' ') if
        not word.startswith('@') and 'http' not in word and not word.startswith('www.')))


def remove_all_multiples():
    df[content] = df[content].apply(lambda x: remove_multiples(x))


def remove_multiples(s):
    finalstr = ""
    i = 0
    while i < len(s):
        count = 1
        if i + 1 < len(s):
            while s[i] == s[i + 1]:
                count += 1
                i += 1
                if i + 1 >= len(s):
                    break
            if count == 2 and s[i].isalpha():
                finalstr += s[i]
                finalstr += s[i]
            elif count > 2 and (s[i] == '!' or s[i] == '?'):
                finalstr += s[i]
            else:
                finalstr += s[i]
        else:
            finalstr += s[i]
        i += 1
    if len(finalstr) != 0:
        if finalstr[0] == ' ':
            finalstr = finalstr[1:]
        if len(finalstr) != 0:
            if finalstr[-1] == ' ':
                finalstr = finalstr[:-1]
    return finalstr


def remove_all_stop_words():
    df[content] = df[content].apply(lambda x: ' '.join(word for word in x.split(' ') if
        word not in stop_words))


def remove_hashtags():
    df[content] = df[content].apply(lambda x: ' '.join(remove_hashtag(word) for word in x.split(' ')))


def remove_hashtag(word):
    if word.startswith('#'):
        word = word[1:]
    return word


def merge_classes():
    #df[sen] = df[sen].apply(lambda x: "boredom" if x == "empty" else x)
    #df[sen] = df[sen].apply(lambda x: "hate" if x == "anger" else x)
    df[sen] = df[sen].apply(lambda x: "enthusiasm" if x == "fun" or x == "surprise" else x)

def balance(df):
    for classtoreduce in classestoreduce:
        print(classtoreduce)
        index = df[(df['sentiment'] == classtoreduce)].index
        if len(index) - num > 0:
            #generate array of random numbers in range 0 to len(index)-1
            locs = random.sample(range(len(index)), num)
            locs.sort(reverse=True)
            for i in locs:
                index = index.delete(i)
            df.drop(index, inplace=True)

    for classtoincrease in classestoincrease:
        rowsdf = df[(df['sentiment'] == classtoincrease)]
        print(classtoincrease)
        if (len(rowsdf) > 0):
            locs = np.random.randint(low=0, high=len(rowsdf), size=(num-len(rowsdf),))
            count = len(rowsdf)
            while count < num:
                for loc in locs:
                    new = rowsdf.iloc[[loc]].copy()
                    idmax = df['tweet_id'].max() + 1
                    new['tweet_id'] = new['tweet_id'].apply(lambda x: idmax)
                    df = pd.concat([df, new], ignore_index=True)
                    count += 1

    for classtoremove in classestoremove:
        print(classtoremove)
        index = df[(df['sentiment'] == classtoremove)].index
        for ind in index:
            df.drop(ind, inplace=True)
    return df


def create_csv():
    df4 = df.copy()
    df4[content] = df4[content].apply(lambda x: ' '.join(PorterStemmer().stem(word) for word in x.split(' ')))
    df4[content] = df4[content].apply(
        lambda x: word_tokenize(x) if len(x.split(' ')) > 1 else str(word_tokenize(x + '. .')))
    df4.to_csv(test1, index=False, encoding='utf8')


df = pd.read_csv(file_path)

stop_words = set((stopwords.words('english')))

classestoreduce = ['worry', 'neutral']
classestoincrease = ['sadness', 'enthusiasm', 'love', 'happiness']
classestoremove = ['relief', 'hate', 'boredom', 'anger', 'empty']
num = 5500

lower()
remove_urls()
remove_hashtags()
remove_symbols()

remove_all_multiples()

remove_all_stop_words()

merge_classes()
df = balance(df)

df[user] = df[user].apply(lambda x: x.lower())

create_csv()

"""
df2 = df.copy()
df2[content] = df2[content].apply(lambda x: ' '.join(LancasterStemmer().stem(word) for word in x.split(' ')))
df2[content] = df2[content].apply(
    lambda x: word_tokenize(x) if len(x.split(' ')) > 1 else str(word_tokenize(x + '. . .')))
df2.to_csv(mergeTLS, index=False, encoding='utf8')
"""
