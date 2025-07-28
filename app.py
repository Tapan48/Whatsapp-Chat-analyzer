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
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter

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
    st.dataframe(df)
    
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
            st.title("👥 Most Active Users")
            
            col1, col2 = st.columns(2)
            df1, df2 = helper.most_busy_users(df)
            
            with col1:
                st.subheader("Message Distribution")
                st.caption("Number of messages sent by top 5 users")

                st.bar_chart(
                    df1,
                    use_container_width=True,
                    height=400
                )
               
            
            with col2:
                st.subheader("Participation % of all members", divider=False)
                st.dataframe(
                    df2,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "User": "Username",
                        "percent(%)": st.column_config.NumberColumn(
                            "Participation %",
                            help="Percentage of total messages",
                            format="%.2f%%"
                        )
                    }
                )
        else:
            st.title(f"👤 {user}'s Participation")
            
            # Calculate this specific user's participation data
            user_messages = df[df["User"] == user].shape[0]
            total_messages = df[df["User"] != "group notification"].shape[0]
            user_percentage = round((user_messages / total_messages) * 100, 2) if total_messages > 0 else 0
            
            # Create a DataFrame for this user's participation
            user_participation_data = pd.DataFrame({
                'User': [user],
                'percent(%)': [user_percentage]
            })
            
            st.subheader("Participation in Group Chat", divider=False)
            st.dataframe(
                user_participation_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "User": "Username",
                    "percent(%)": st.column_config.NumberColumn(
                        "Participation %",
                        help="Percentage of total messages",
                        format="%.2f%%"
                    )
                }
            )
            
            # Add some additional insights
            st.subheader("📊 User Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Messages", user_messages)
            with col2:
                st.metric("Total Group Messages", total_messages)
            with col3:
                st.metric("Participation %", f"{user_percentage}%")
        st.title("Word Cloud")
        df_wc = helper.word_cloud(user, df)
        
        # Create a better word cloud visualization
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')  # Remove axes for cleaner look
        
        # Add title and styling
        plt.tight_layout(pad=0)
        
        # Display the word cloud
        st.pyplot(fig)
        
        # Add word cloud insights and statistics
        st.subheader("📊 Word Cloud Insights")
        
        # Get word frequency data for insights
        temp = df[df["User"] != "group notification"]
        final_df = temp[temp["Message"] != "<Media omitted>"]
        
        if user != "Overall":
            final_df = final_df[final_df["User"] == user]
        
        # Count words for insights
        words = []
        for message in final_df["Message"]:
            words.extend(message.lower().split())
        
        word_counts = Counter(words)
        total_words = len(words)
        unique_words = len(word_counts)
        
        # Display insights in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Words", f"{total_words:,}")
        with col2:
            st.metric("Unique Words", f"{unique_words:,}")
        with col3:
            st.metric("Most Frequent Word", word_counts.most_common(1)[0][0] if word_counts else "N/A")
        with col4:
            st.metric("Most Frequent Count", word_counts.most_common(1)[0][1] if word_counts else 0)
        
        # Add word cloud features explanation
        st.subheader("🎨 Word Cloud Features")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📏 Size**: Larger words = More frequent usage
            **🎨 Colors**: Different colors for visual appeal
            **📝 Content**: Excludes common stop words
            **👥 Scope**: Shows words for selected user/overall
            """)
        
        with col2:
            st.markdown("""
            **📊 Frequency**: Word size indicates usage frequency
            **🎯 Focus**: Highlights most important words
            **📈 Insights**: Visual representation of chat patterns
            """)
        
        # Show top words in a compact format
        if word_counts:
            st.subheader("🏆 Top 10 Most Frequent Words")
            top_words = word_counts.most_common(10)
            
            # Create a nice display
            cols = st.columns(5)
            for idx, (word, count) in enumerate(top_words):
                col_idx = idx % 5
                with cols[col_idx]:
                    st.markdown(f"**{word}**")
                    st.markdown(f"*{count} times*")
        
        st.title("Top 20 most used words")
        top_20_words = helper.top_20_most_words(df, user)
        
        # Create a better visualization with Plotly
        fig = go.Figure()
        
        # Add horizontal bar chart with better styling
        fig.add_trace(go.Bar(
            y=top_20_words[0],  # Words
            x=top_20_words[1],  # Counts
            orientation='h',
            marker=dict(
                color=top_20_words[1],  # Color by count
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Count")
            ),
            hovertemplate='<b>%{y}</b><br>' +
                         'Count: %{x}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title="Top 20 Most Used Words",
            xaxis_title="Word Count",
            yaxis_title="Words",
            height=600,  # Taller for better readability
            showlegend=False,
            yaxis=dict(
                autorange="reversed",  # Show most used at top
                tickfont=dict(size=12)
            ),
            xaxis=dict(
                tickfont=dict(size=10)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add summary statistics
        st.subheader("📊 Word Usage Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Most Used Word", top_20_words.iloc[0, 0] if len(top_20_words) > 0 else "N/A")
        with col2:
            st.metric("Most Used Count", top_20_words.iloc[0, 1] if len(top_20_words) > 0 else 0)
        with col3:
            st.metric("Average Word Count", f"{top_20_words[1].mean():.1f}" if len(top_20_words) > 0 else "0.0")
        with col4:
            st.metric("Total Unique Words", len(top_20_words))
        
        # Show top 20 words in a clean table
        st.subheader("📋 Complete Top 20 Words List")
        words_df = pd.DataFrame({
            'Rank': range(1, len(top_20_words) + 1),
            'Word': top_20_words[0],
            'Count': top_20_words[1]
        })
        st.dataframe(words_df, use_container_width=True)
        
        
        st.title("Monthly-Timeline")
        monthly_msges = helper.monthly_timeline(df, user)
        
        # Create interactive Plotly chart for monthly timeline
        fig = go.Figure()
        
        # Add line plot with all data points
        fig.add_trace(go.Scatter(
            x=monthly_msges["month-year"],
            y=monthly_msges["Message"],
            mode='lines+markers',
            name='Messages',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, color='#1f77b4'),
            hovertemplate='<b>%{x}</b><br>' +
                         'Messages: %{y}<br>' +
                         '<extra></extra>'
        ))
        
        # Highlight peak month
        peak_idx = monthly_msges["Message"].idxmax()
        fig.add_trace(go.Scatter(
            x=[monthly_msges["month-year"][peak_idx]],
            y=[monthly_msges["Message"][peak_idx]],
            mode='markers',
            name='Peak Month',
            marker=dict(size=15, color='red', symbol='star'),
            hovertemplate='<b>Peak Month: %{x}</b><br>' +
                         'Messages: %{y}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title="Monthly Message Timeline",
            xaxis_title="Month-Year",
            yaxis_title="Messages",
            hovermode='closest',
            showlegend=True,
            height=500,
            xaxis=dict(
                tickangle=45,
                tickmode='array',
                ticktext=monthly_msges["month-year"],
                tickvals=list(range(len(monthly_msges)))
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add monthly summary statistics
        st.subheader("📊 Monthly Activity Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Months", len(monthly_msges))
        with col2:
            st.metric("Average Messages/Month", f"{monthly_msges['Message'].mean():.1f}")
        with col3:
            st.metric("Peak Month Messages", monthly_msges["Message"].max())
        with col4:
            st.metric("Peak Month", monthly_msges["month-year"][peak_idx])
        
        # Show most busy months in a table
        st.subheader("🏆 Top 5 Busiest Months")
        top_months = monthly_msges.nlargest(5, 'Message')[['month-year', 'Message']]
        top_months.columns = ['Month-Year', 'Messages']
        # Add proper indexing (1, 2, 3, etc.)
        top_months = top_months.reset_index(drop=True)
        top_months.index = top_months.index + 1
        st.dataframe(top_months, use_container_width=True)

        st.title("Daily-Timeline")
        daily_msges = helper.daily_timeline(user, df)
        
        # Create better daily timeline alternatives
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Weekly Activity Pattern")
            # Use existing weekly_activity function
            weekly_pattern = helper.weekly_activity(user, df)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=weekly_pattern.index,
                y=weekly_pattern.values,
                marker_color='lightblue',
                hovertemplate='<b>%{x}</b><br>Messages: %{y}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Messages by Day of Week",
                xaxis_title="Day of Week",
                yaxis_title="Total Messages",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Activity Distribution")
            # Create activity level distribution
            activity_levels = pd.cut(daily_msges['Message'], 
                                   bins=[0, 10, 50, 100, float('inf')], 
                                   labels=['Low (0-10)', 'Medium (11-50)', 'High (51-100)', 'Very High (100+)'])
            activity_dist = activity_levels.value_counts()
            
            fig = go.Figure()
            fig.add_trace(go.Pie(
                labels=activity_dist.index,
                values=activity_dist.values,
                hole=0.4,
                hovertemplate='<b>%{label}</b><br>Days: %{value}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Activity Level Distribution",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Add summary statistics
        st.subheader("📈 Daily Activity Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Active Days", len(daily_msges))
        with col2:
            st.metric("Average Messages/Day", f"{daily_msges['Message'].mean():.1f}")
        with col3:
            st.metric("Peak Day Messages", daily_msges['Message'].max())
        with col4:
            st.metric("Most Active Day", weekly_pattern.index[0] if len(weekly_pattern) > 0 else "N/A")
        
        # Show top 10 busiest days in a table
        st.subheader("🏆 Top 10 Busiest Days")
        top_days = daily_msges.nlargest(10, 'Message')[['onlydate', 'Message']]
        top_days.columns = ['Date', 'Messages']
        # Add proper indexing (1, 2, 3, etc.)
        top_days = top_days.reset_index(drop=True)
        top_days.index = top_days.index + 1
        st.dataframe(top_days, use_container_width=True)
        
        
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
                st.dataframe(emoji_df.reset_index(drop=True).assign(index=lambda x: x.index + 1).set_index('index'), use_container_width=True)
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
        
        