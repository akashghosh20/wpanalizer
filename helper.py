def fetchStat(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    return num_messages, len(words),num_media_messages
    # if selected_user=="Overall":
    #     num_messages = df.shape[0]
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())
    #     return num_messages,len(words)
    # else:
    #     new_df = df[df['user']==selected_user]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split())
    #     return num_messages,len(words)