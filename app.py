import streamlit as st
import preprocessor,helper
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import seaborn as sns
import tempfile
import setuptools
import boto3
from botocore.exceptions import NoCredentialsError
import os
import uuid
from dotenv import load_dotenv
import emoji

# Configure matplotlib for better emoji support
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'AppleGothic', 'sans-serif']
plt.rcParams['font.size'] = 12


# load_dotenv()  # Load environment variables from the .env file

# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_REGION = os.getenv('AWS_REGION')
# S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')



# s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)


# Function to list all files in the  S3 bucket
# def list_files_in_bucket():
#     try:
#         response = s3_client.list_objects(Bucket=S3_BUCKET_NAME)
#         files = [obj['Key'] for obj in response.get('Contents', [])]

#         if len(files) > 0:
#             st.header("Files in S3 bucket:")
#             for file in files:
#                 st.write(file)
#         else:
#             st.warning("No files found in the S3 bucket.")

#     except Exception as e:
#         st.error(f"An error occurred while listing objects in S3: {str(e)}")


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose whatsapp text file")

# list_files_button = st.button("List Files in S3 Bucket")

# if list_files_button:
#     list_files_in_bucket()
    
if uploaded_file is not None:
    
    try:
        # Get the current working directory
        currpath = os.getcwd()
        file=uploaded_file.name
            # Generate a random filename
        random_filename = str(uuid.uuid4()) + '.txt'
        
        # Create the full file path
        filename = os.path.join(currpath,file)

        # Upload the file to S3
        # s3_client.upload_file(filename, S3_BUCKET_NAME, random_filename)

        # print("File uploaded successfully to S3!")
        # st.write("File uploaded successfully to S3!")

    except Exception as e:
        print(f"An error occurred while uploading the file to S3: {str(e)}")
        st.write(f"An error occurred while uploading the file to S3: {str(e)}")
   
        
        
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
     # Decode bytes into string
    string_data = bytes_data.decode('utf-8')
    
    df=preprocessor.preprocess(string_data)
    # st.dataframe(df)
    
    users=df["User"].unique().tolist()
    
    
    if "group notification" in users:
       users.remove("group notification")
    else:
       pass
    
    users.sort()
    users.insert(0,"Overall")
    
    user=st.sidebar.selectbox("Show analysis wrt",users)
    
    num_messages,num_words,no_media_msgs,no_links=helper.fetch_stats(user, df)
   

    
    
    
    if st.sidebar.button("Show analysis"):
        # try:
        #     # Upload the temporary text file to S3
        #    s3_client.upload_file(temp_file_path, S3_BUCKET_NAME, uploaded_file.name)
        #    st.success(f"File '{uploaded_file.name}' uploaded to S3 successfully!")
        # except NoCredentialsError:
        #     st.error("AWS credentials not found. Make sure you've configured them correctly.")
        # except Exception as e:
        #     st.error(f"An error occurred while uploading to S3: {e}")
        
        # try:
        #     # Upload the temporary text file to S3
        #     with open(temp_file_path, 'rb') as temp_file:
        #         s3_client.upload_fileobj(io.BytesIO(temp_file.read()), S3_BUCKET_NAME, uploaded_file.name)
        #     st.success(f"File '{uploaded_file.name}' uploaded to S3 successfully!")
        # except NoCredentialsError:
        #     st.error("AWS credentials not found. Make sure you've configured them correctly.")
        # except Exception as e:
        #     st.error(f"An error occurred while uploading to S3: {e}")
            
            
            
        
        st.title(uploaded_file.name)
        
            
        col1, col2, col3,col4= st.columns(4)

        with col1:
            
            st.header("Total messages")
            st.title(num_messages)
           
            
        with col2:
            
            st.header("Total words")
            st.title(num_words)
            
        with col3:
            
            st.header("Media Shared")
            st.title(no_media_msgs) 
            
        with col4:
            
            st.header("Links Shared")
            st.title(no_links)           
       
        if user=="Overall":
            st.title("Most busy Users")
            
            col1, col2= st.columns(2)
            df1,df2=helper.most_busy_users(df)
            
            with col1:
                               
                                
                 st.bar_chart(df1)
              
            with col2:
                st.dataframe(df2)
                
        st.title("Word Cloud")
        df_wc = helper.word_cloud(user, df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        st.title("Top 20 most used words")
        top_20_words=helper.top_20_most_words(df,user)
        fig, ax = plt.subplots()



        ax.barh(top_20_words[0], top_20_words[1])
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)
        
        
        st.title("Monthly-Timeline")
        
        monthly_msges=helper.monthly_timeline(df,user)
        fig, ax = plt.subplots()



        ax.plot(monthly_msges["month-year"], monthly_msges["Message"])
        plt.xticks(rotation= 'vertical')
        plt.figure(figsize=(100,30))
        st.pyplot(fig)
        
        
        
        st.title("Daily-Timeline")
        daily_msges=helper.daily_timeline(user,df)
        fig, ax = plt.subplots()



        ax.plot(daily_msges["onlydate"], daily_msges["Message"])
        plt.xticks(rotation= 'vertical')
        plt.figure(figsize=(100,30))
        st.pyplot(fig)
        
        
        st.title("Activity Map")
        col1, col2= st.columns(2)
        
        
        with col1:
            st.header("Most busy day")
            
            busyday=helper.weekly_activity(user,df)
        
            
            fig, ax = plt.subplots()
            ax.bar(busyday.index, busyday.values)
            plt.xticks(rotation= 'vertical')
            plt.figure(figsize=(100,60))
            st.pyplot(fig)

        
        with col2:
            st.header("Most busy Month")
            
            busymonth=helper.monthly_activity(user,df)
            fig, ax = plt.subplots()
            ax.bar(busymonth.index, busymonth.values,color="orange")
            plt.xticks(rotation= 'vertical')
            plt.figure(figsize=(100,60))
            st.pyplot(fig)
            
        st.title("Weekly Activity Map")    
        user_heatmap=helper.activity_heatmap(user,df)   
        fig, ax = plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
        # Emoji Analysis Section
        st.title("Emoji Analysis")
        emoji_df, emoji_stats = helper.emoji_analysis(df, user)
        
        if not emoji_df.empty:
            # Statistics in a nice grid layout
            st.header("📊 Emoji Usage Statistics")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Messages", emoji_stats["total_messages"])
            with col2:
                st.metric("Messages with Emojis", emoji_stats["messages_with_emojis"])
            with col3:
                st.metric("Emoji Usage Rate", f"{emoji_stats['emoji_usage_rate']:.1f}%")
            with col4:
                st.metric("Total Emojis Used", emoji_stats["total_emojis"])
            with col5:
                st.metric("Unique Emojis", emoji_stats["unique_emojis"])
            
            # Top emojis display
            st.header("🏆 Top Emojis Used")
            if len(emoji_df) > 0:
                # Show top 10 emojis in a simple format
                top_10 = emoji_df.head(10)
                cols = st.columns(5)
                for idx, row in top_10.iterrows():
                    col_idx = idx % 5
                    with cols[col_idx]:
                        st.write(f"**{row['Emoji']}**")
                        st.write(f"**{row['Count']} times**")
            
            # All emojis in a scrollable format
            st.header("📋 Complete Emoji List")
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 Table View", "🎯 Grid View", "📝 Text List"])
            
            with tab1:
                st.dataframe(emoji_df, use_container_width=True)
            
            with tab2:
                # Grid display with simple format
                cols = st.columns(4)
                for idx, row in emoji_df.iterrows():
                    col_idx = idx % 4
                    with cols[col_idx]:
                        st.write(f"**{row['Emoji']}**")
                        st.write(f"{row['Count']} times")
            
            with tab3:
                # Simple text list
                emoji_text = ""
                for idx, row in emoji_df.iterrows():
                    emoji_text += f"{row['Emoji']} ({row['Count']})  "
                    if (idx + 1) % 6 == 0:  # New line every 6 emojis
                        emoji_text += "\n"
                
                st.text_area("All Emojis Used:", emoji_text, height=200)
            
            # Emoji insights - using simple Streamlit components
            st.header("💡 Emoji Insights")
            if len(emoji_df) > 0:
                most_used = emoji_df.iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🥇 Most Used Emoji")
                    st.write(f"**{most_used['Emoji']}**")
                    st.write(f"**{most_used['Count']} times**")
                
                with col2:
                    st.subheader("📊 Emoji Diversity")
                    st.write(f"**{emoji_stats['unique_emojis']}**")
                    st.write("Unique emojis used")
        else:
            st.warning("No emojis found in messages")
            st.info("Try uploading a chat file that contains emoji messages.")
        
        