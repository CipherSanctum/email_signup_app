from celery import shared_task
from django.core.mail import send_mail
from .models import EmailListPerson


@shared_task
def signup_email(unconf_email_id):
    """ Task to send an email notification when user signs up to email list. """
    # SMTP EXAMPLE:
    unconf_email = EmailListPerson.objects.get(id=unconf_email_id)
    unconf_email_link = 'https://www.YourWebsite.com/email_signup/{}/{}/'.format(unconf_email.id, unconf_email.random_uuid)
    subject = 'Please confirm your email address.'
    message = 'Someone just tried to sign up to my email list with this email. If it was you, please go to the following link to confirm it, otherwise ignore this email.\n\n{}'.format(unconf_email_link)
    mail_sent = send_mail(subject, message, 'donotreply@YourWebsite.com', [unconf_email.email])
    return mail_sent
