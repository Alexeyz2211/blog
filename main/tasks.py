from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_email_notice(users):
    send_mail('New post added!',
              'user add new post',
              'alexey221190@gmail.com',
              users)
    print('done')
    return None