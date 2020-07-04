# import datetime
import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import EmailListSubscriber


@admin.register(EmailListSubscriber)
class ConfirmEmailAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'email_sub_name', 'is_confirmed', 'joined', 'emails_sent', 'category']
    list_filter = ('is_confirmed', 'category')
    search_fields = ('user_email',)
    actions = ['export_confirmed_to_csv', 'export_unconfirmed_to_csv', 'export_all_to_csv', 'make_confirmed', 'make_unconfirmed']

    def export_confirmed_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;' 'filename=confirmed_emails.csv'
        writer = csv.writer(response)

        # write a first row
        writer.writerow(['Email', 'email_sub_name', 'is_confirmed', 'joined', 'emails_sent', 'random_uuid'])

        # write data in rows
        for subscriber in queryset.filter(is_confirmed=True):
            writer.writerow([subscriber.user_email, subscriber.email_sub_name, subscriber.is_confirmed, subscriber.joined, subscriber.emails_sent, subscriber.random_uuid])
        return response

    export_confirmed_to_csv.short_description = 'Export selected CONFIRMED to CSV'

    def export_unconfirmed_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;' 'filename=unconfirmed_emails.csv'
        writer = csv.writer(response)

        # write a first row
        writer.writerow(['Email', 'email_sub_name', 'is_confirmed', 'joined', 'emails_sent', 'random_uuid'])

        # write data in rows
        for subscriber in queryset.filter(is_confirmed=False):
            writer.writerow([subscriber.user_email, subscriber.email_sub_name, subscriber.is_confirmed, subscriber.joined, subscriber.emails_sent, subscriber.random_uuid])
        return response

    export_unconfirmed_to_csv.short_description = 'Export selected UNCONFIRMED to CSV'

    def export_all_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;' 'filename=all_emails.csv'
        writer = csv.writer(response)

        # write a first row
        writer.writerow(['Email', 'email_sub_name', 'is_confirmed', 'joined', 'emails_sent', 'random_uuid'])

        # write data in rows
        for subscriber in queryset:
            writer.writerow([subscriber.user_email, subscriber.email_sub_name, subscriber.is_confirmed, subscriber.joined, subscriber.emails_sent, subscriber.random_uuid])
        return response

    export_all_to_csv.short_description = 'Export ALL selected to CSV'

    def make_confirmed(self, request, queryset):
        rows_updated = queryset.update(is_confirmed=True)
        if rows_updated >= 1:
            self.message_user(request, '{} users CONFIRMED'.format(queryset.count()))

    make_confirmed.short_description = 'Confirm selected users'

    def make_unconfirmed(self, request, queryset):
        rows_updated = queryset.update(is_confirmed=False)
        if rows_updated >= 1:
            self.message_user(request, '{} users UNCONFIRMED'.format(queryset.count()))

    make_unconfirmed.short_description = 'Unconfirm selected users'
