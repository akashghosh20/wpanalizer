import streamlit as st
import re
import pandas as pd


def preprocess(datas):
    messages = []
    dates = []

    pattern = r'(\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\u202f[ap]m) - (.+)'

    for data in datas.split('\n'):
        message_match = re.match(pattern, data)
        if message_match:
            date = message_match.group(1)
            message = message_match.group(2)
            dates.append(date)
            messages.append(message)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    cleaned_messages = []
    for message in df['user_message']:
        cleaned_message = re.sub(r'^\w+\s\w+:\s', '', message)
        cleaned_messages.append(cleaned_message)

    df['message'] = cleaned_messages

    users = []
    for message in df["user_message"]:
        match = re.match(r'^(.*?):', message)
        if match:
            user = match.group(1)
            users.append(user)
        else:
            user = "group_notification"
            users.append(user)

    df['user'] = users

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p')
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    return df



