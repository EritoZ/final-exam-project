from celery import shared_task
from django.core.mail import send_mail

from DjangoForum import settings


def email_message():
    message = '''
    Click the link to confirm your account.
    
    
    '''


@shared_task
def send_email(user_email):
    send_mail(
        subject='Confirmation Email',
        message=f'{email_message()}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email,],
    )
