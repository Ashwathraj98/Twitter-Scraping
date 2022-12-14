import snscrape.modules.twitter as sntwitter
import pandas as pd
#import pymongo
from pymongo import MongoClient
import datetime
import streamlit as st

st.set_page_config(page_title='Twitter scraper')

st.subheader("""Let's scrape some Tweets""")

tweet_tag = st.sidebar.text_input("Enter the Twitter hashtag")
if tweet_tag == "":
    st.stop()
nftweet = st.sidebar.number_input('Insert a number of tweets to search', min_value=1, max_value=100000, value = 10, step=1)

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.sidebar.date_input('Start date',today)
end_date = st.sidebar.date_input('End date',tomorrow)

if (st.sidebar.button('Submit')):
    if start_date < end_date:
        st.success('Data Extracted!')

        tweets_list = []
        for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(f'#{tweet_tag} since:{start_date} until:{end_date}').get_items()):
            if i > nftweet:
                break
            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.lang, tweet.source, tweet.likeCount])
        tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Reply', 'Retweet', 'Lang','Source', 'Likes'])

        st.write(tweets_df)
                def convert_df(tweets_df):
            return tweets_df.to_csv(index=False).encode('utf-8')
        csv = convert_df(tweets_df)
        tweets_df.to_csv('text-query-tweets.csv', sep=',', index=False)
        json_string = tweets_df.to_json(orient='index')
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.download_button("Download JSON File", json_string, "tweets.json", "application/json", key='download-json')
        with col2:
            if st.button('Upload To Database'):
                client = MongoClient("mongodb://localhost:27017/")
                db = client["TW_scrap"]
                tweets_df = db["keywords"]
                data_dict = tweets_df.to_dict("records")
                tweets_df.insert_many(data_dict)
            

        with col3:
            st.download_button("Download CSV File", csv, "tweets.csv", "text/csv", key='download-csv')
    else:
        st.error('Error')
