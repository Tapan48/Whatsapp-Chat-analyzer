from urlextract import URLExtract
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
import setuptools
import pandas as pd
import emoji 
from textblob import TextBlob
import nltk
import numpy as np
from datetime import datetime, timedelta
extractor = URLExtract()

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def fetch_stats(user,df):
    
    if user=="Overall":
        
        no_media_msgs=df[df["Message"]=="<Media omitted>"].shape[0]
        links=[]

        for message in df["Message"]:
            links.extend(extractor.find_urls(message))
        
        words = []
        for i, row in df.iterrows():
            if row["User"] != "group notification":
                message_words = row["Message"].split()
                words.extend(message_words)
                
        df=df[df["User"]!="group notification"]     
        
        return df.shape[0],len(words),no_media_msgs,len(links)
    else:
        
        newdf=df[df["User"]==user]
    
        user_noof_msgs=newdf.shape[0]
        
        
        no_media_msgs=newdf[newdf["Message"]=="<Media omitted>"].shape[0]
        links=[]
        
        for message in newdf["Message"]:
            links.extend(extractor.find_urls(message))
        
       
        words = []
        for i, row in newdf.iterrows():
            
                message_words = row["Message"].split()
                words.extend(message_words)
        return user_noof_msgs,len(words),no_media_msgs,len(links)
   
   
def most_busy_users(df):
    
    df1=df["User"].value_counts().head()
    
    # Calculate participation percentages for all users
    participation_df = round((df["User"].value_counts()/df.shape[0])*100,2).reset_index()
    
    # Debug: print the actual column names
    print("Original columns:", participation_df.columns.tolist())
    print("DataFrame head:", participation_df.head())
    
    # After reset_index(), the columns are 'User' (user names) and 'count' (percentages)
    # We need to rename 'count' to 'Participation %'
    participation_df = participation_df.rename(columns={"count":"Participation %"})
    
    print("After renaming columns:", participation_df.columns.tolist())
    
    return df1, participation_df   #### df1 contains data of top 5 users and their  messages_count,  participation_df consists of users and their percentage of messages
    
def word_cloud(user,df):
    f=open("stop_hinglish.txt","r")
    stop_words=f.read()
    
    temp=df[df["User"]!="group notification"]
    final_df=temp[temp["Message"]!="<Media omitted>"]
    
    
    def remove_stopwords(message):
    
        words=[]

                  ###### remove stop words
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word) 
        return " ".join(words)        
                    
                    
    
    if user=="Overall":
        
        final_df_copy = final_df.copy()
        final_df_copy.loc[:, "Message"]=final_df_copy["Message"].apply(remove_stopwords)

        # Create a WordCloud object with the desired parameters
        wc = WordCloud(width=800, height=800,min_font_size=10, background_color='white')
        df_wc =wc.generate(final_df_copy['Message'].str.cat(sep=" "))
        
        
        
    
    else:
        newdf=final_df[final_df["User"]==user].copy()
        newdf.loc[:, "Message"]=newdf["Message"].apply(remove_stopwords)
   
        

        # Create a WordCloud object with the desired parameters
        wc = WordCloud(width=800, height=800, min_font_size=10, background_color='white')
        df_wc=wc.generate(newdf['Message'].str.cat(sep=" "))
    
    return df_wc    
     
        
            
def top_20_most_words(df,user):
    temp=df[df["User"]!="group notification"]
    final_df=temp[temp["Message"]!="<Media omitted>"]
    f=open("stop_hinglish.txt","r")
    stop_words=f.read()
    
    
    if user=="Overall":
    
        
        words=[]

        for message in final_df["Message"]:             ###### remove stop words
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)    
                    
        newdf=pd.DataFrame(Counter(words).most_common(20)) 
        
    else:
        final_df=final_df[final_df["User"]==user]
        words=[]

        for message in final_df["Message"]:             ###### remove stop words
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)    
                    
        newdf=pd.DataFrame(Counter(words).most_common(20))
        
        
               
    return newdf     


def emojis_get():
    pass  

def monthly_timeline(df,user):
        
        df_copy = df.copy()
        df_copy['MonthNum'] = df_copy['datetime'].dt.month

        
    
        if user!="Overall":
            
            df_copy=df_copy[df_copy["User"]==user]
            
        
                
        timeline=df_copy.groupby(["year","month","MonthNum"]).count()["Message"].reset_index()
        time=[]
        for i in range(timeline.shape[0]):

           time.append(timeline["month"][i]+"-"+ str(timeline["year"][i]))
        
        timeline["month-year"]=time
        
        return timeline
    
def daily_timeline(user,df):
    
    df_copy = df.copy()
    if user!="Overall":
            
            df_copy=df_copy[df_copy["User"]==user]
            
    df_copy["onlydate"]=df_copy["datetime"].dt.date
    daily=df_copy.groupby(["onlydate"]).count()["Message"].reset_index()
    return daily        
    
def weekly_activity(user,df):
    df_copy = df.copy()
    if user!="Overall":
            
            df_copy=df_copy[df_copy["User"]==user]
            
    df_copy["day_name"]=df_copy["datetime"].dt.day_name()
       
    
    return df_copy["day_name"].value_counts()                                 
    
def monthly_activity(user,df): 
    df_copy = df.copy()
    if user!="Overall":
            
        df_copy=df_copy[df_copy["User"]==user]
            
     
      
   
    return df_copy["month"].value_counts()                                    
       
def activity_heatmap(selected_user,df):
    
    df_copy = df.copy()
    if selected_user != 'Overall':
        df_copy = df_copy[df_copy['User'] == selected_user]

    user_heatmap = df_copy.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap    
     
            
            
            
def emoji_analysis(df, user):
    """Analyze emoji usage patterns in messages"""
    
    # Filter for specific user or overall
    if user != "Overall":
        df = df[df["User"] == user]
    else:
        # For overall, exclude group notifications like fetch_stats does
        df = df[df["User"] != "group notification"]
    
    # Store original df for total message count (including media)
    original_df = df.copy()
    total_messages = original_df.shape[0]
    
    # Filter out media messages for emoji analysis
    df = df[df["Message"] != "<Media omitted>"]
    
    emoji_counts = {}
    messages_with_emojis = 0
    
    # Go through each message
    for message in df["Message"]:
        # Find all emojis in the message
        emojis = emoji.emoji_list(message)
        
        if emojis:  # If message contains emojis
            messages_with_emojis += 1
            
        # Count each emoji
        for e in emojis:
            emoji_char = e["emoji"]
            emoji_counts[emoji_char] = emoji_counts.get(emoji_char, 0) + 1
    
    # Convert to DataFrame for easy display
    if emoji_counts:
        emoji_df = pd.DataFrame(list(emoji_counts.items()), 
                               columns=["Emoji", "Count"])
        emoji_df = emoji_df.sort_values("Count", ascending=False)
    else:
        emoji_df = pd.DataFrame(columns=["Emoji", "Count"])
    
    # Calculate emoji usage statistics
    emoji_stats = {
        "total_messages": total_messages,
        "messages_with_emojis": messages_with_emojis,
        "emoji_usage_rate": (messages_with_emojis / total_messages * 100) if total_messages > 0 else 0,
        "total_emojis": sum(emoji_counts.values()),
        "unique_emojis": len(emoji_counts)
    }
    
    return emoji_df, emoji_stats    
     
            
            
            
def sentiment_analysis(df, user):
    """Analyze sentiment of messages"""
    
    # Filter for specific user or overall
    if user != "Overall":
        df = df[df["User"] == user]
    else:
        # For overall, exclude group notifications like fetch_stats does
        df = df[df["User"] != "group notification"]
    
    # Store original df for total message count (including media)
    original_df = df.copy()
    total_messages = original_df.shape[0]
    
    # Filter out media messages for sentiment analysis
    df = df[df["Message"] != "<Media omitted>"]
    
    sentiment_scores = []
    emotions = []
    positive_messages = 0
    negative_messages = 0
    neutral_messages = 0
    
    for message in df["Message"]:
        if message.strip():
            # Get sentiment score using TextBlob
            blob = TextBlob(message)
            sentiment_score = blob.sentiment.polarity
            
            # Classify sentiment
            if sentiment_score > 0.1:
                sentiment_class = "Positive"
                positive_messages += 1
            elif sentiment_score < -0.1:
                sentiment_class = "Negative"
                negative_messages += 1
            else:
                sentiment_class = "Neutral"
                neutral_messages += 1
            
            # Classify emotion based on sentiment and keywords
            emotion = classify_emotion(message, sentiment_score)
            
            sentiment_scores.append({
                'message': message,
                'sentiment_score': sentiment_score,
                'sentiment_class': sentiment_class,
                'emotion': emotion,
                'datetime': df[df["Message"] == message]["datetime"].iloc[0] if len(df[df["Message"] == message]) > 0 else None
            })
            emotions.append(emotion)
    
    # Calculate sentiment statistics
    if sentiment_scores:
        avg_sentiment = np.mean([s['sentiment_score'] for s in sentiment_scores])
        sentiment_stats = {
            "total_messages": total_messages,
            "positive_messages": positive_messages,
            "negative_messages": negative_messages,
            "neutral_messages": neutral_messages,
            "positive_percentage": (positive_messages / total_messages * 100) if total_messages > 0 else 0,
            "negative_percentage": (negative_messages / total_messages * 100) if total_messages > 0 else 0,
            "neutral_percentage": (neutral_messages / total_messages * 100) if total_messages > 0 else 0,
            "average_sentiment": avg_sentiment,
            "sentiment_variance": np.var([s['sentiment_score'] for s in sentiment_scores])
        }
        
        # Create emotion distribution
        emotion_counts = Counter(emotions)
        emotion_df = pd.DataFrame(list(emotion_counts.items()), columns=["Emotion", "Count"])
        emotion_df = emotion_df.sort_values("Count", ascending=False)
        
        # Create sentiment timeline
        sentiment_df = pd.DataFrame(sentiment_scores)
        if not sentiment_df.empty and 'datetime' in sentiment_df.columns:
            sentiment_df = sentiment_df.dropna(subset=['datetime'])
            sentiment_df['date'] = sentiment_df['datetime'].dt.date
            daily_sentiment = sentiment_df.groupby('date')['sentiment_score'].mean().reset_index()
            daily_sentiment.columns = ['Date', 'Average_Sentiment']
        else:
            daily_sentiment = pd.DataFrame(columns=['Date', 'Average_Sentiment'])
        
    else:
        sentiment_stats = {
            "total_messages": total_messages,
            "positive_messages": 0,
            "negative_messages": 0,
            "neutral_messages": 0,
            "positive_percentage": 0,
            "negative_percentage": 0,
            "neutral_percentage": 0,
            "average_sentiment": 0,
            "sentiment_variance": 0
        }
        emotion_df = pd.DataFrame(columns=["Emotion", "Count"])
        daily_sentiment = pd.DataFrame(columns=['Date', 'Average_Sentiment'])
    
    return sentiment_df, emotion_df, daily_sentiment, sentiment_stats

def classify_emotion(message, sentiment_score):
    """Classify emotion based on sentiment score and keywords"""
    
    message_lower = message.lower()
    
    # Define emotion keywords
    joy_keywords = ['happy', 'great', 'awesome', 'amazing', 'wonderful', 'excellent', 'love', 'lol', 'haha', '😊', '😄', '😍', '🎉', '❤️']
    sadness_keywords = ['sad', 'sorry', 'miss', 'missed', 'alone', 'lonely', 'cry', '😢', '😭', '💔', '😞']
    anger_keywords = ['angry', 'mad', 'hate', 'terrible', 'awful', 'horrible', 'fuck', 'shit', 'damn', '😠', '😡', '💢']
    fear_keywords = ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified', '😨', '😰', '😱']
    surprise_keywords = ['wow', 'omg', 'unbelievable', 'incredible', 'shocked', '😲', '😯', '😱']
    disgust_keywords = ['disgusting', 'gross', 'ew', 'yuck', '🤢', '🤮']
    
    # Check for emotion keywords
    if any(keyword in message_lower for keyword in joy_keywords):
        return "Joy"
    elif any(keyword in message_lower for keyword in sadness_keywords):
        return "Sadness"
    elif any(keyword in message_lower for keyword in anger_keywords):
        return "Anger"
    elif any(keyword in message_lower for keyword in fear_keywords):
        return "Fear"
    elif any(keyword in message_lower for keyword in surprise_keywords):
        return "Surprise"
    elif any(keyword in message_lower for keyword in disgust_keywords):
        return "Disgust"
    
    # Classify based on sentiment score if no keywords found
    if sentiment_score > 0.3:
        return "Joy"
    elif sentiment_score < -0.3:
        return "Sadness"
    else:
        return "Neutral"

def user_sentiment_profiles(df):
    """Analyze sentiment profiles for all users"""
    
    users = df["User"].unique()
    user_profiles = []
    
    for user in users:
        if user != "group notification":
            user_df = df[df["User"] == user]
            user_messages = user_df[user_df["Message"] != "<Media omitted>"]
            
            if len(user_messages) > 0:
                # Calculate sentiment for this user
                sentiment_scores = []
                for message in user_messages["Message"]:
                    if message.strip():
                        blob = TextBlob(message)
                        sentiment_scores.append(blob.sentiment.polarity)
                
                if sentiment_scores:
                    avg_sentiment = np.mean(sentiment_scores)
                    positive_count = sum(1 for score in sentiment_scores if score > 0.1)
                    negative_count = sum(1 for score in sentiment_scores if score < -0.1)
                    neutral_count = len(sentiment_scores) - positive_count - negative_count
                    
                    user_profiles.append({
                        'User': user,
                        'Total_Messages': len(sentiment_scores),
                        'Average_Sentiment': avg_sentiment,
                        'Positive_Messages': positive_count,
                        'Negative_Messages': negative_count,
                        'Neutral_Messages': neutral_count,
                        'Positive_Percentage': (positive_count / len(sentiment_scores) * 100) if len(sentiment_scores) > 0 else 0,
                        'Negative_Percentage': (negative_count / len(sentiment_scores) * 100) if len(sentiment_scores) > 0 else 0,
                        'Neutral_Percentage': (neutral_count / len(sentiment_scores) * 100) if len(sentiment_scores) > 0 else 0
                    })
    
    return pd.DataFrame(user_profiles)

def sentiment_trends(df, user):
    """Analyze sentiment trends over time"""
    
    # Filter for specific user or overall
    if user != "Overall":
        df = df[df["User"] == user]
    
    # Filter out media messages
    df = df[df["Message"] != "<Media omitted>"]
    
    # Add sentiment scores
    sentiment_scores = []
    for message in df["Message"]:
        if message.strip():
            blob = TextBlob(message)
            sentiment_scores.append(blob.sentiment.polarity)
        else:
            sentiment_scores.append(0)
    
    df['sentiment_score'] = sentiment_scores
    
    # Group by different time periods
    df['date'] = df['datetime'].dt.date
    df['week'] = df['datetime'].dt.isocalendar().week
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour
    
    # Daily sentiment trends
    daily_sentiment = df.groupby('date')['sentiment_score'].agg(['mean', 'count']).reset_index()
    daily_sentiment.columns = ['Date', 'Average_Sentiment', 'Message_Count']
    
    # Weekly sentiment trends
    weekly_sentiment = df.groupby('week')['sentiment_score'].agg(['mean', 'count']).reset_index()
    weekly_sentiment.columns = ['Week', 'Average_Sentiment', 'Message_Count']
    
    # Monthly sentiment trends
    monthly_sentiment = df.groupby('month')['sentiment_score'].agg(['mean', 'count']).reset_index()
    monthly_sentiment.columns = ['Month', 'Average_Sentiment', 'Message_Count']
    
    # Hourly sentiment patterns
    hourly_sentiment = df.groupby('hour')['sentiment_score'].agg(['mean', 'count']).reset_index()
    hourly_sentiment.columns = ['Hour', 'Average_Sentiment', 'Message_Count']
    
    return daily_sentiment, weekly_sentiment, monthly_sentiment, hourly_sentiment
     
            
            
            