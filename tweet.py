import snscrape.modules.twitter as sntwitter
import streamlit as st
import pandas as pd
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["mytweetdata"]
mycol = mydb["lic.corp"]

tweets_list = []
for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper('LIC corporation since:2021-10-16 until:2022-10-16').get_items()):
    if i > 1000:

        break
    tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount])
tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username','Reply','Retweet','Lang','Source','Likes'])

twdata = tweets_df.to_dict("records")
x = mycol.insert_one({"scrapedata":twdata})
#for x in mycol.find():
    #print(x)

st.set_page_config(page_title='Twitter scraper')
st.image('twitty.png')
st.subheader("""Let's scrape some Tweets""")

with st.form(key='Twitter_form'):
    search_term = st.text_input('What do you want to search for?')
    limit = st.slider('How many tweets do you want to get?', 0, 500, step=20)
    output_csv = st.radio('Save a CSV file?', ['Yes', 'No'])
    file_name = st.text_input('Name the CSV file:')
    submit_button = st.form_submit_button(label='Search')

st.dataframe(tweets_df)

stramlit run tweet.py