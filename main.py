import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt
import wordcloud
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    datas = bytes_data.decode('utf-8')
    df = preprocessing.preprocess(datas)
    st.dataframe(df)
    # fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis with respect to",user_list)

    if st.sidebar.button("Analysis"):

        num_messages,words,num_of_media = helper.fetchStat(selected_user,df)
        col1, col2, col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_of_media)

        if selected_user == "Overall":
            st.title("Most Busy Users")
            x,new_df = helper.MostBusiest(df)
            fig,ax = plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title("Time Analysis")
        timeline = helper.timeAnalysis(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df = helper.MostCommonWord(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)


        # counting emoji
        result_df = helper.emoji_frequency(selected_user, df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(result_df)
        with col2:
            fig,ax = plt.subplots()
            custom_colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#c2c2f0', '#ffb3e6']
            ax.pie(result_df['Frequency'],labels=result_df['Emoji'],colors=['red','green','blue','violet','indigo','yellow'],autopct="%0.2f")
            st.pyplot(fig)


        st.title("Daily Timeline analysis")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        plt.figure(figsize=(18, 10))
        plt.xticks(rotation='vertical')
        ax.bar(daily_timeline['only_date'], daily_timeline['message'])
        st.pyplot(fig)