from django import forms
from django.utils.translation import gettext_lazy as _
from .models import EmailListSubscriber


class EmailListSubscriberForm(forms.ModelForm):
    class Meta:
        model = EmailListSubscriber
        fields = ('email_sub_name', 'user_email')
        widgets = {
                    'user_email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
                    'email_sub_name': forms.TextInput(attrs={'placeholder': 'optional name'})
                }
        labels = {'user_email': _('Your Email'), 'email_sub_name': _('Your email')}


    # FOR CUSTOM VALIDATION ONLY!!!!
    # def clean_email(self):
    #     email = self.cleaned_data.get('user_email')
    #     if not "gmail.com" in email:
    #         raiso forms.ValidationError("Email has to be at gmail.com")
    #     return email
