from celery import shared_task
from .models import Post
import requests
import os
from django.conf import settings
from datetime import datetime
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def send_scheduled_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        # print(f"Sending caption: {post.caption}")
        # logger.info(f"Sending caption: {post.caption}")

        # channel_name = '@myeditbot'

        # caption = ""
        # def send_text(url, chat_id, caption):
        #     print("**********")
        #     try:
        #         response = requests.post(url, json={'chat_id': chat_id, 'text': caption})
        #         print(response.text)
        #         print("************")
        #     except Exception as e:
        #         print(e)
        #
        # final_line = post.caption
        # print(final_line)
        # apiURL = f'https://tapi.bale.ai/bot{apiToken}/sendPhoto'
        # send_text(apiURL, '@taknegar', final_line)
        # print("4444444444444444")
        #
        # post.delete()

        # $#############################
        image_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
        apiToken = '776054248:lGIjwIrJIZD76PAygxvgZhTt81vQkoSlpGPA1Mat'
        apiURL = f'https://tapi.bale.ai/bot{apiToken}/SendPhoto'
        print("*************")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        print("*************")

        for channel in post.channels.all():
            chat_id = channel.channel_id  # مثلاً "@my_channel" یا "-1001234567890"
            print(chat_id)
            print("*************")
            caption = post.caption
            # ارسال تصویر
            # with open(image_path, 'rb') as image_file:
            #     photo = image_file
            #     chat_id = '@taknegar'
            #     # print(chat_id)
            #     photo = r'F:\sourcecode\distributed\chbackend\posts\celebrity_WSDIdbi.png'
            #     caption = 'test'
            #     print("*************")
            #     print(chat_id)

                # data = {
                #     'chat_id': chat_id,
                #     'caption': post.caption
                # }
                # response = requests.post(apiURL, json={'chat_id': '@taknegar', 'caption': caption}, files = {'photo': photo})
            response = requests.post(apiURL, data={'chat_id': chat_id, 'caption': caption},
                                files={'photo': open(image_path, 'rb')})
                # response.text
                # response = requests.post(
                #     apiURL,
                #     photo,
                #     chat_id,
                #     caption
                # )
            print("*************")



            # بررسی موفقیت ارسال
            if response.status_code != 200:
                raise Exception(f"Failed to send to {chat_id}: {response.text}")

        os.remove(image_path)
        post.delete()

        ################################

        # ارسال عکس و کپشن از طریق API تلگرام
        # url = f"https://api.telegram.org/bot {settings.TELEGRAM_BOT_TOKEN}/sendPhoto"
        # url = f'https://tapi.bale.ai/bot{apiToken}/sendMessage'

        # with open(os.path.join(settings.MEDIA_ROOT, str(post.image)), 'rb') as image_file:
        #     files = {'photo': image_file}
        #
        #     data = {'chat_id': post.channels.first().channel_id, 'caption': post.caption}
        #     response = requests.post(url, data=data, post.caption)
        #
        # if response.status_code == 200:
        #     post.sent = True
        #     post.save()
        # else:
        #     print("Failed to send via Telegram API")

    except Exception as e:
        # print("not allowed")
        print(f"Error: {str(e)}")
        post.sent = False
        post.save()


@shared_task
def check_scheduled_posts():
    now = timezone.now()
    posts = Post.objects.filter(scheduled_time__lte=now, sent=False)
    for post in posts:
        send_scheduled_post.delay(post.id)
