import random
import numpy as np
import pandas as pd
from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

file_path = 'test.csv'
content = 'content'
user = 'author'
sen = 'sentiment'

testres = 'testres2.csv'


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
            elif count >2 and (s[i] == '!' or s[i] == '?'):
                finalstr += s[i]
            else:
                finalstr += s[i]
        else:
            finalstr += s[i]
        i += 1
    if len(finalstr) != 0:
        if finalstr[0] == ' ':
            finalstr = finalstr[1:]
        if finalstr[-1] == ' ':
            finalstr = finalstr[:-1]

    return finalstr


def hashtag(word):
    if word.startswith('#'):
        word = word[1:]
    return word


df = pd.read_csv(file_path)

classestoreduce = ['love', 'sadness', 'happiness', 'worry', 'neutral', 'enthusiasm', 'empty', 'hate', 'relief', 'fun', 'surprise']
classestoincrease = ['anger', 'boredom']
classestoremove = ['relief', 'hate', 'boredom']

num = 2


def balance(df):
    for classtoreduce in classestoreduce:
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
        index = df[(df['sentiment'] == classtoremove)].index
        df.drop(index, inplace=True)


df[sen] = df[sen].apply(lambda x: "boredom" if x == "empty" else x)
df[sen] = df[sen].apply(lambda x: "hate" if x == "angry" else x)
df[sen] = df[sen].apply(lambda x: "enthusiasm" if x == "fun" or x == "surprise" else x)

df[user] = df[user].apply(lambda x: x.lower())

df[content] = df[content].apply(lambda x: x.lower())
df[content] = df[content].apply(lambda x: ' '.join(
    word for word in x.split(' ') if not word.startswith('@') and 'http' not in word and not word.startswith('www.')))
df[content] = df[content].apply(lambda x: ' '.join(hashtag(word) for word in x.split(' ')))
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
df[content] = df[content].apply(lambda x: remove_multiples(x))

balance(df)

df4 = df.copy()
df4[content] = df4[content].apply(lambda x: ' '.join(PorterStemmer().stem(word) for word in x.split(' ')))
df4[content] = df4[content].apply(
    lambda x: word_tokenize(x) if len(x.split(' ')) > 1 else str(word_tokenize(x + '. . .')))
df4.to_csv(testres, index=False, encoding='utf8')
