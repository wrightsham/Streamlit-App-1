from pprint import pprint
import json
import requests
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

import main_functions

nltk.download("punkt")
nltk.download("stopwords")
api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["my_key"]
my_articles = main_functions.read_from_file("JSON_Files/responses.json")
my_articles2 = main_functions.read_from_file("JSON_Files/responses3.json")
#--------------------Streamlit--------------
st.title("Welcome to NYT Word Cloud Generator.")

st.title("Project 1")
st.write("Displays for the user the frequency distribution for the top 10 most "
         "common words used in the top stories of the topic selected.")
st.header("Part A - Top Stories API")
st.write("1 - Topic Selection")
user_name = ""
user_name = st.text_input("Enter your name below",user_name)

option = st.selectbox(
    "Select a topic of interest",
    ["","Arts", "Automobiles", "Books", "Business", "Fashion", "Food", "Health", "Home",
     "Insider", "Magazine", "Movies", "NY Region", "Obituaries", "Opinion", "Politics",
     "Real Estate", "Science", "Sports", "Sunday Review", "Technology", "Theater",
     "T-magazine", "Travel", "Upshot", "US", "World"]
)

if user_name not in [""] and option not in "":
    st.write("Hello, " + user_name + "! You selected " + option + ".")

option_l = option.lower()
option_w = option_l.replace(" ","")

if option_w not in "":
    url = "https://api.nytimes.com/svc/topstories/v2/" + option_w + ".json?api-key=" + api_key
    response = requests.get(url).json()
    main_functions.save_to_file(response, "JSON_Files/responses.json")
#---------------------------------------------------------------------------------------------------------------
str1 = ""

for i in my_articles["results"]:
    str1 = str1 + i["abstract"]

sentences = sent_tokenize(str1)

words = word_tokenize(str1)

words_no_punc = []

for w in words:
    if w.isalpha():
        words_no_punc.append(w.lower())

stopwords = stopwords.words("english")

clean_words = []

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

fdist = FreqDist(clean_words)
#----------------------------------------------------------------------------------------------------------------
st.write("2 - Frequency Distribution")
checked = st.checkbox("Click here to generate the word frequency distribution.")

if checked:
    chartData = pd.DataFrame(fdist.most_common(10),columns=['word', 'frequency'])
    # st.table(chartData)
    #https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html
    fig = plt.figure(figsize=(10,8))
    plt.gcf().subplots_adjust(bottom=0.15)
    fdist.plot(10, cumulative=False, color ="black")
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title('Frequency Distribution for ' + option)
    # plt.show()
    st.pyplot(fig)
    # fig.savefig('freqDist.png', bbox_inches = "tight")
    # st.image('freqDist.png')

st.write("3 - Wordcloud")
checked1 = st.checkbox("Click here to generate the wordcloud.")

if checked1:
    wordcloud = WordCloud().generate_from_frequencies(fdist)
    fig, ax = plt.subplots()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig)
    st.write("Wordcloud generated for the " + option + " topic.")

st.header("Part B - Most Popular Articles")
st.write("This will generate a wordcloud for the most shared, emailed or viewed articles.")

option2 = st.selectbox(
    "Select your set of articles:",
    ["","Shared", "Emailed", "Viewed"]
)

option2 = option2.lower()

option3 = st.selectbox(
    "Select a time period (days):",
    ["","1","7","30"]
)

if option2 not in "" and option3 not in "":
    url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + option2 + "/" + option3 + ".json?api-key=" + api_key
    response = requests.get(url2).json()
    main_functions.save_to_file(response, "JSON_Files/responses3.json")
    str2 = ""

    for p in my_articles2["results"]:
        str2 = str2 + p["abstract"]

    sentences = sent_tokenize(str2)
    words = word_tokenize(str2)

    words_no_punc = []

    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    clean_words = []

    for w in words_no_punc:
        if w not in stopwords:
            clean_words.append(w)

    fdist2 = FreqDist(clean_words)

    wordcloud2 = WordCloud().generate_from_frequencies(fdist2)
    fig, ax = plt.subplots()
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig)