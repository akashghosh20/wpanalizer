from wordcloud import WordCloud
import pandas as pd
import re
def fetchStat(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    return num_messages, len(words),num_media_messages

def MostBusiest(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def MostCommonWord(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]

    words = []

    for message in df['message']:
        words.extend(message.split())

    from collections import Counter
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

# def count_emojis(selected_user,df,message):
#     if selected_user!="Overall":
#         df = df[df['user'] == selected_user]
#     emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]'
#     emojis = re.findall(emoji_pattern, message)
#     return emojis
#
#
# # Example messages
#     df = pd.DataFrame({'message': df['message']})
#
#     emoji_freq = {}
#     for message in df['message']:
#         emojis = count_emojis(message)
#         for emoji in emojis:
#             if emoji in emoji_freq:
#                 emoji_freq[emoji] += 1
#             else:
#                 emoji_freq[emoji] = 1
#
#     emoji_df = pd.DataFrame({'Emoji': list(emoji_freq.keys()), 'Frequency': list(emoji_freq.values())})
#     emoji_df = emoji_df.sort_values(by='Frequency', ascending=False)
#     return emoji_df

# In helper.py



def count_emojis(message):
    emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]'
    emojis = re.findall(emoji_pattern, message)
    return emojis


def emoji_frequency(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emoji_freq = {}
    for message in df['message']:
        emojis = count_emojis(message)
        for emoji in emojis:
            if emoji in emoji_freq:
                emoji_freq[emoji] += 1
            else:
                emoji_freq[emoji] = 1

    emoji_df = pd.DataFrame({'Emoji': list(emoji_freq.keys()), 'Frequency': list(emoji_freq.values())})
    emoji_df = emoji_df.sort_values(by='Frequency', ascending=False)
    return emoji_df.head(6)

def timeAnalysis(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    df['month_num'] = df['message_date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    times = []
    for i in range(timeline.shape[0]):
        times.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = times
    return timeline
def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    df['only_date'] = df['message_date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
