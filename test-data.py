import pandas as pd
import requests
from datetime import datetime
import re

# خواندن فایل اکسل
df = pd.read_excel(r"C:\Users\User\Downloads\output-8d0a296694116378a1290f39.xlsx")

# API‌ها
AUTHORS_API = "http://192.168.115.31:3000/api/authors/"
CHANNELS_API = "http://192.168.115.31:3000/api/channel-code/"


# تابع برای استخراج هشتگ‌ها از متن
def extract_hashtags(text):
    # print(text)
    try:
        hashtags = re.findall(r'#[\w\d_]+', text)
    except Exception as e:
        print(e)
        hashtags = ''
    return ' '.join(hashtags)


# تابع برای یافتن کد نویسنده
def get_author_code(username):
    response = requests.get(f"{AUTHORS_API}?search={username}")
    if response.status_code == 200 and response.json():
        return response.json()[0]['id']
    return 0  # کد نامشخص


# تابع برای یافتن کد کانال
def get_channel_code(channel_name):
    response = requests.get(f"{CHANNELS_API}?search={channel_name}")
    if response.status_code == 200 and response.json():
        return response.json()[0]['id']
    return 0  # کد نامشخص


# پردازش هر ردیف از داده‌ها
for index, row in df.iterrows():
    post_data = {
        "channel": get_author_code(row['نام کاربری منبع']),
        "author": get_author_code(row['نام کاربری منبع']),
        "post_text": str(row['متن مطلب']),
        "hashtags": extract_hashtags(row['متن مطلب']),
        "views": row['مشاهده مطلب'],
        "collected_at": row['زمان ایجاد میلادی'].split()[0]  # فقط تاریخ
    }

    # ارسال درخواست POST
    response = requests.post("http://192.168.115.31:3000/api/posts/", json=post_data)
    print(f"Row {index + 1} - Status Code: {response.status_code}")

    # break