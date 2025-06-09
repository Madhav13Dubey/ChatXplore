import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

from helper import most_common_words, daily_timeline, activity_heatmap

st.set_page_config(page_title="Chat Analyzer")

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # as this file is in stream(byte data) so we have to encode it into a string
    data = bytes_data.decode("utf-8")
    # st.text(data)              # we can the text after encoding
    df = preprocessor.preprocess(data)   # take up of data from preprocessor and preprocessing it

   #   st.dataframe(df)  # display of dataframe

   # we are using dropdown that will select particular user (present in the group)
    # dropdown (userlevel and grouplevel)

    #1. fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()  # in ascending order
    user_list.insert(0,"Overall")    # rather than to show we show overall chatting from starting position i.e 0
    selected_user = st.sidebar.selectbox("Show Analysis w.r.t", user_list) # here we can see the respective user


    if st.sidebar.button("Show Analysis w.r.t"):    # after clicking show analysis start do analysis
       # Stats Area
       num_messages, words, num_media_message, num_links  =  helper.fetch_stats(selected_user,df)

       st.title("Top Statistics")
       col1, col2, col3, col4 = st.columns(4)

       with col1:
         st.header("Total Messages")
         st.title(num_messages)

       with col2:
           st.header("Total Words")
           st.title(words)

       with col3:
           st.header("Media Shared")
           st.title(num_media_message)

       with col4:
           st.header("Links Shared")
           st.title(num_links)
       # Monthly TimeLine
       st.title("Monthly Timeline")
       timeline = helper.monthly_timeline(selected_user, df)
       fig,ax = plt.subplots()
       ax.plot(timeline['time'], timeline['message'],color='purple')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

      # Daily Timeline
       st.title('Daily Timeline')
       daily_timeline = helper.daily_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

     # most active days (Activity Day)
       st.title("Activity Map")
       col1, col2 = st.columns(2)

       with col1:
           st.header("Most Busy Day")
           busy_day = helper.week_activity_map(selected_user, df)
           fig,ax = plt.subplots()
           ax.bar(busy_day.index,busy_day.values)
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

       with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

       # finding the time period for the user who present most active in the particular time of instane using heatmap
       st.title("Weekly Activity Map")
       user_heatmap = helper.activity_heatmap(selected_user, df)
       fig,ax = plt.subplots()
       ax = sns.heatmap(user_heatmap)
       st.pyplot(fig)

       # finding the  busiest user in the entire group
       if selected_user == 'Overall':
           st.title(" Most Busy Users")
           x, new_df = helper.most_bust_users(df)
           fig, ax = plt.subplots()
           col1, col2 = st.columns(2)

           with col1:
               ax.bar(x.index, x.values, color='red')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

           with col2:
               st.dataframe(new_df)

        # Making of WordCloud
       st.title("Word Cloud")
       df_wc = helper.create_wordcloud(selected_user, df)
       fig, ax = plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)

       # most common words used
       most_common_df = helper.most_common_words(selected_user, df)
       fig,ax = plt.subplots()

       ax.barh(most_common_df[0], most_common_df[1])    # on x axis and on y axis on horizontal bar chart
       plt.xticks(rotation=0)        # printing the numeric value horizontally
       st.title('Most Common Words')

       st.pyplot(fig)
       # st.dataframe(most_common_df)
       # Emoji Analysis
       st.title("Emoji Analysis")
       emoji_df = helper.emoji_helper(selected_user, df)

       if emoji_df.empty:  # Check if the DataFrame is empty
           st.write("No emojis were sent in the chat.")
       else:
           col1, col2 = st.columns(2)
           with col1:
               st.dataframe(emoji_df)

           with col2:
               fig, ax = plt.subplots()
               ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
               st.pyplot(fig)
