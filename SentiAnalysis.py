import tweepy
import re
import pandas as pd
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pprint
from subprocess import check_output
import string
import numpy as np
import io
import os
import unicodedata
from unidecode import unidecode


class final():
    __consumer_key = 'xxxx'
    __consumer_secret = 'xxxx'
    __access_key = 'xxxx'
    __access_secret = 'xxxx'
    final_tweet_list = []
    final_class_list = []
    def __init__(self,date):
        self.cols = ['tweet', 'class']
        self.stop_words = set(stopwords.words('english'))
        # this is the auth creditianls
        self.auth = tweepy.OAuthHandler(self.__consumer_key, self.__consumer_secret)
        self.auth.set_access_token(self.__access_key, self.__access_secret)
        self.api = tweepy.API(self.auth)
        # this is the starting date , we change it randomly
        self.start_date = date
        self.tweetList = []
        self.classLabel = []
        # Emoji patterns
        self.emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
    # def clean_tweet(self,tweet):

    def clean_tweet(self,tweet):
        print("<-*Cleaning the Tweet*->\n")
        # we created the tokens
        word_tokens = word_tokenize(tweet)

        # removing : after removing mentions and removing retweet symbol
        tweet = re.sub(r':', '', tweet)
        tweet = re.sub(r'‚Ä¶', '', tweet)

        tweet = re.sub(r'@[A-Za-z0-9]+','',tweet) # replacing mentions
        tweet = re.sub('https?://[A-Za-z0-9./]+','',tweet) #replacing https links in the data

        # replace consecutive non-ASCII characters with a space
        tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)

        tweet = self.emoji_pattern.sub(r'', tweet) # emojis removing

        emoticons_happy = set([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
            '<3'
        ])

        # Sad Emoticons
        emoticons_sad = set([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
            ':c', ':{', '>:\\', ';('
        ])
        emoticons = emoticons_happy.union(emoticons_sad)
        filtered_tweet = [w for w in word_tokens if w not in self.stop_words]
        filtered_tweet = [w for w in filtered_tweet if w not in emoticons]
        filtered_tweet = [w for w in filtered_tweet if w not in string.punctuation]

        return ' '.join(filtered_tweet)

    def storetocsv(self):
        self.final_tweet_list += self.tweetList
        self.final_class_list += self.classLabel

    def checkscore(self,text):

        ob = check_output(
            'java -jar SentiStrength.jar sentidata C:\\Users\\mvsp\\Desktop\\senti\\SentiStrength_DataEnglishFeb2017\\ '
            'text ' + text.replace(" ", "+"), cwd='C:\\Users\\mvsp\\Desktop\\senti\\')

        l = list(ob.rstrip())
        if l[0] == 45:
            num1 = -(l[1] - 48)
            num2 = l[3] - 48
        else:
            num2 = -(l[3] - 48)
            num1 = l[0] - 48
        ls = []
        ls.append(num1)
        ls.append(num2)
        lap = np.array(ls)
        value = lap[np.argmax(np.abs(lap))]

        return value

    def lemmtext(self,text):
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        return ' '.join([lem.lemmatize(word) for word in text.split()])

    def deemojify(self,text):
        returnString = ""

        for character in text:
            try:
                character.encode("ascii")
                returnString += character
            except UnicodeEncodeError:
                pass

        return returnString

    def removestuff(self,text):
        wordtokens = text.split()
        stuff = "[]_-+=><;:|!./?,~`*\\$#@^&{}()\'\""
        num = "0123456789"

        l = ' '.join([''.join([c for c in word if c not in stuff]) for word in wordtokens])


        wordtokens = l.split()

        l = []
        for word in wordtokens:
            newword = ""
            for w in word:
                if w in num:
                    break
                else:
                    newword += w

            if newword != "":
                l.append(newword)

        return ' '.join(l)

    def final_save(self):
        d={"text":self.final_tweet_list,"class":self.final_class_list}
        df = pd.DataFrame(d)
        file3 = "C:\\Users\\mvsp\\Documents\\SentimentalAnalysis\\sam\\train_3rd.csv"
        df.to_csv(file3, mode='a', index=False, encoding='utf-8')
        print("completed\n")

    def gather_data(self,keyword):

        for page in tweepy.Cursor(self.api.search, q=keyword,count=200, include_rts=False, since=self.start_date).pages(10):
            for status in page:
                if status.lang != 'en': #if not english skip the tweet
                    continue

                clean_text = p.clean(status.text) # basic preprocessing

                deemoji = self.deemojify(clean_text)

                fil_text = self.clean_tweet(deemoji)

                fil_text = self.lemmtext(fil_text)

                fil_text = self.removestuff(fil_text)
                print(fil_text+"\n")

                if fil_text != "" and fil_text not in self.tweetList:
                    self.tweetList.append(fil_text)

                    score = self.checkscore(fil_text)

                    print(str(score)+"\n")
                    self.classLabel.append(score)

        self.storetocsv()


obj = final('2020-04-23')
obj.gather_data('#lockdownextension')
obj = final('2020-04-16')
obj.gather_data('#lockdownextension')
obj = final('2020-04-09')
obj.gather_data('#lockdownextension')
obj = final('2020-04-02')
obj.gather_data('#lockdownextension')
obj = final('2020-03-26')
obj.gather_data('#lockdownextension')

fin = final('2020-11-20')
fin.final_save()