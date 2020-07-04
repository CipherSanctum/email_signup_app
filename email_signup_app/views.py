from django.shortcuts import render  # redirect
from django.core.mail import get_connection, send_mail  #, get_connection
from django.core.mail.message import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from .forms import EmailListSubscriberForm
from .models import EmailListSubscriber
# from .tasks import signup_email  # delete_email
from project_root.local_settings import (EMAIL_HOST, EMAIL_PORT,
                                            EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
                                            EMAIL_USE_SSL)


def email_signup_home(request):
    form = EmailListSubscriberForm(request.POST or None)
    if request.method == 'POST':
        try:
            attempted_email = request.POST.get('user_email', False).lower()
            this_person = EmailListSubscriber.objects.get(user_email=attempted_email)
            if this_person.is_confirmed:
                return render(request, 'email_signup_app/confirmation_check.html', {'already_confirmed': True})
            elif (this_person.user_email == attempted_email) and (not this_person.is_confirmed):
                return render(request, 'email_signup_app/confirmation_check.html', {'remind_check_email': True})
        except ObjectDoesNotExist:
            if form.is_valid():
                unconf_user = form.save(commit=False)
                unconf_user.user_email = attempted_email
                unconf_user.name = request.POST.get('email_sub_name', False).title()
                unconf_user.save()
                request.session.setdefault('email_list_conf_sent', 'An email has already been sent')    # can acces in template from request.session.email_signup, so it's visible on every page... Just put it in base.html, and
                                                                                                  # write the form raw so you don't need special form for every view

                # Send email when testing offline...
                # send_mail('Please confirm your email subscription to MyWebsite.com',
                #           'Just click the link below and follow the directions\n\nhttps://www.MyWebsite.com/email_signup_app/{}/{}/'.format(unconf_user.id, unconf_user.random_uuid),
                #           'donotreply@YourWebsite.com',
                #           [unconf_user.user_email],
                #           fail_silently=False)

                # Send email when live
                with get_connection(host=EMAIL_HOST, port=EMAIL_PORT, username=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD, use_ssl=EMAIL_USE_SSL) as connection:
                    EmailMessage('Please confirm your email subscription to MyWebsite.com',
                                'Just click the link below and follow the directions\n\nhttps://www.MyWebsite.com/email_signup_app/{}/{}/'.format(unconf_user.id, unconf_user.random_uuid),
                                'donotreply@YourWebsite.com',
                                [unconf_user.user_email],
                                headers={'List-Subscribe': '<{}>'.format(unconf_user.user_email)},
                                connection=connection).send()

                return render(request, 'email_signup_app/confirmation_check.html', {'email_sent': True})
    return render(request, 'email_signup_app/confirmation_check.html', {'form': form})


def email_signup_confirm(request, unconf_email_id, random_uuid):
    unconf_email = EmailListSubscriber.objects.get(id=unconf_email_id)
    if request.method == 'POST':
        new_email = unconf_email
        new_email.is_confirmed = True
        new_email.save()
        request.session.pop('email_list_conf_sent', None)
        request.session.setdefault('email_list_confirmed', 'Thanks for signing up!')
        return render(request, 'email_signup_app/confirmation_check.html', {'signed_up': True})
    return render(request, 'email_signup_app/confirmation_check.html', {'unconf_email': unconf_email})


def email_unsubscribe(request, conf_email_id, random_uuid):
    this_subscriber = EmailListSubscriber.objects.get(id=conf_email_id)
    form = EmailListSubscriberForm(request.POST or None)
    if request.method == 'POST':
        prove_user_email = request.POST.get('user_email', False).lower()
        if prove_user_email == this_subscriber.user_email:
            this_subscriber.delete()
            return render(request, 'email_signup_app/confirmation_check.html', {'removed': True})
        else:
            return render(request, 'email_signup_app/confirmation_check.html', {'email_doesnt_exist': True, 'this_subscriber': this_subscriber, 'form': form})
    return render(request, 'email_signup_app/confirmation_check.html', {'wants_to_unsub': True, 'this_subscriber': this_subscriber, 'form': form})
