from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from DjangoForum import settings

User = get_user_model()


def email_message(url):

    message = f'''
    Click the link to confirm your account.
    {url}
    '''

    return message


@shared_task
def send_email(url, user_id):
    user = User.objects.get(id=user_id)

    send_mail(
        subject='Confirmation Email - Reddem',
        message=f'{email_message(url)}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email,],
    )
