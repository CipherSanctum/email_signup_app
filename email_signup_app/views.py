from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import EmailSignupForm
from .models import EmailListPerson, EmailListPersonDelete
from .tasks import signup_email
from captcha_app.models import CaptchaNumber


def email_signup_home(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == 'POST':
        attempted_email = request.POST.get('email', False).lower()
        try:
            check_email = EmailListPerson.objects.get(email=attempted_email)
            if check_email.status_choices == 'confirmed':
                return render(request, 'email_signup_app/confirmation_check.html', {'already_confirmed': check_email})
            elif check_email.status_choices == 'unconfirmed':
                random_img = CaptchaNumber.objects.order_by('?').first()
                return render(request, 'email_signup_app/confirmation_check.html', {'dont_send_twice': check_email, 'random_img': random_img})
        except ObjectDoesNotExist:
            if form.is_valid():
                add_unconf_email = EmailListPerson()
                add_unconf_email.email = attempted_email
                add_unconf_email.save()
                signup_email.delay(add_unconf_email.id)
                return redirect('email_signup_app:email_signup_go_check')
    return render(request, 'email_signup_app/home.html', {'form': form})


def email_signup_go_check(request):
    return render(request, 'email_signup_app/home.html', {'go_check_email': 'Please go check your email to confirm it.'})


def email_signup_confirm(request, unconf_email_id, random_uuid):
    unconf_email = EmailListPerson.objects.get(id=unconf_email_id)
    if request.method == 'POST':
        conf_email = unconf_email
        conf_email.status_choices = 'confirmed'
        conf_email.save()
        return redirect(reverse('email_signup_app:email_signup_done', args=[conf_email.id, conf_email.random_uuid, conf_email.rand_int]))
    return render(request, 'email_signup_app/confirmation_check.html', {'unconf_email': unconf_email})


def email_signup_done(request, conf_email_id, random_uuid, rand_int):
    conf_email = EmailListPerson.objects.get(id=conf_email_id)
    if request.method == 'POST':
        if conf_email.email == request.POST.get('email', False).lower():
            conf_email.times_downloaded = 0
            conf_email.save()
            return render(request, 'email_signup_app/done.html', {'reset_times_downloaded': 'Your limit has been reset'})
        else:
            return render(request, 'email_signup_app/done.html', {'wrong_email': 'Wrong email'})
    if conf_email.times_downloaded <= 2:
        conf_email.times_downloaded += 1
        conf_email.save()
        return render(request, 'email_signup_app/done.html', {'signed_up': 'Thanks for signing up!'})
    else:
        return render(request, 'email_signup_app/done.html', {'too_many_times': 'You have been here too many times'})


def email_list_remove(request, conf_email_id, random_uuid):
    """
        WHY I DO NOT ALLOW USERS TO conf_email.delete() HERE:
            Assume you had 20 EmailListPerson's.... Since the admin action slice's the list by the status_choices='confirmed'
            attribute, if you modify this list before the campaign is done sending to everyone on it, you are likely to end up with people receiving doubles,
            or no email at all. Doubles can hurt your sending reputation among receiving mail servers, and reduce your ability to get messages
            to their inbox. And no emails = no notice. So both are bad.
        EXAMPLE:
            original_list = [0:10]
            # you send to original_list on day 1, and [0:4] delete themselves right after sending...
            # day 2 comes, and you send to [10:21], thinking your whole list has been emailed...
            # But python sees original_list as what the original [4:14] would have been (4-13), which is 10 people,
            # it's correct to do so, and you just skipped sending to objects 10-13 without knowing it, because
            # the 2nd day, [10:21] became what the original [14:21] would have been.
        SOLUTION:
            Run the admin action to delete people who want off your sending list AFTER your campaign is completely done sending to
            everyone on it.
    """
    conf_email = EmailListPerson.objects.get(id=conf_email_id)
    if request.method == 'POST':
        check_user = request.POST.get('remove_email', False).lower()
        if (check_user == conf_email.email) and (conf_email.status_choices == 'confirmed'):
            request_removal = EmailListPersonDelete()
            request_removal.email = conf_email.email
            request_removal.save()
            return redirect('email_signup_app:email_list_remove_done')
        else:
            return render(request, 'email_signup_app/remove_email_check.html', {'wrong_email': 'Wrong email'})
    return render(request, 'email_signup_app/remove_email_check.html')


def email_list_remove_done(request):
    return render(request, 'email_signup_app/remove_email_check.html', {'removed': 'You have been successfully removed from the email list'})
