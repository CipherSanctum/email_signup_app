from django.contrib import admin
from django.core.mail import send_mass_mail
from .models import EmailListPerson, EmailListPersonDelete, EmailCampaign


@admin.register(EmailListPerson)
class EmailListPersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'status_choices', 'random_uuid', 'rand_int', 'times_downloaded']
    list_editable = ['status_choices']
    list_filter = ['status_choices']
    list_per_page = 50


@admin.register(EmailListPersonDelete)
class EmailListPersonDeleteAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    list_per_page = 25
    actions = ['remove_emails_from_list']

    def remove_emails_from_list(self, request, queryset):
        """
            HOW TO USE THIS METHOD:
                Once you install this, go to the admin panel, click the option in 'Email Signup App' for deleting people, and read the directions
                on that page. You won't see any 'Action' button unless you create an object for that page.
        """
        if request.user.is_superuser:
            confirmed_removals = EmailListPersonDelete.objects.all()
            confirmed_people = EmailListPerson.objects.filter(status_choices='confirmed')
            people_deleted = 0
            for remove_me in confirmed_removals:
                for person in confirmed_people:
                    if remove_me.email == person.email:
                        remove_me.delete()
                        person.delete()
                        people_deleted += 1
        return self.message_user(request, "You have successfully deleted {} from your list".format(people_deleted))
    remove_emails_from_list.short_description = 'Remove ALL people here from your email list. DO NOT USE BEFORE CAMPAIGN SENDING IS COMPLETED'


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'start_point', 'end_point']
    list_editable = ['start_point', 'end_point']
    list_filter = ['created']
    list_per_page = 10
    search_fields = ['title', 'body']
    actions = ['send_email_campaign']

    def send_email_campaign(self, request, queryset):
        """
            Admin only task to send an email to all users on confirmed list.

            EXPLANATION FOR ARGUMENTS OF send_mass_mail() AS DATATUPLE PARAMETER:
                message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
                message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])
                send_mass_mail((message1, message2), fail_silently=False)

                # Message 1 will show both emails in it's list to each person it's sent to. Message 2 will not. To prevent message 1's behavior,
                # make sure the 'datatuple' argument uses a for loop to create a different message for each user, all in a tuple.
                # For this reason, below, I use some_var = tuple(email_list) to put each email as a tuple within a tuple.
        """
        if request.user.is_superuser:
            confirmed_list = EmailListPerson.objects.filter(status_choices='confirmed')  # this is the queryset parameter. Errors without it. No need to call it 'queryset'
            selected_campaign = request.POST.get('_selected_action', None)
            email_campaign = EmailCampaign.objects.get(id=selected_campaign)
            start_point = email_campaign.start_point
            end_point = email_campaign.end_point
            email_list = []

            for email in confirmed_list[start_point:end_point]:
                # Build the message
                subject = email_campaign.title
                message = email_campaign.body + '\n\n\nGo here to unsubscribe to my email list:' + '\n' + 'https://www.YourWebsite.com/email_signup/{}/{}/remove/'.format(email.id, email.random_uuid)  # can put raw html in here with a template, if desired???
                add_person_to_list = (subject, message, 'email_campaign@YourWebsite.com', [email.email])
                email_list.append(add_person_to_list)

            all_emails_separated_tuple = tuple(email_list)
            send_all_emails = send_mass_mail(all_emails_separated_tuple, fail_silently=False)
            return send_all_emails, self.message_user(request, "Emails have been / are currently being sent for the ***{}*** campaign created on ***{}***, to the people\
                                                                on your email list between {} and {}.".format(email_campaign.title, email_campaign.created, start_point, end_point)
                                                     )
    send_email_campaign.short_description = 'Send selected campaign to emails from start point to end point on your confirmed email list'
