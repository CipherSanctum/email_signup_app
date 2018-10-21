from django import forms
# from .models import EmailCampaign


class EmailSignupForm(forms.Form):
    email = forms.EmailField(
                label='Email',
                min_length=5,
                max_length=100,
                widget=forms.EmailInput(
                    attrs={
                        'id': 'email_signup',
                        'placeholder': 'Put your email here...',
                        'class': 'inputbox disp_block center_input_10px_margin_top',
                    }
                )
            )


# THE FOLLOWING IS NOT YET IMPLEMENTED, OR WRITTEN CORRECTLY...
# A radio button should override the default check box on the admin page for
# better efficiency.

# class EmailCampaignAdminForm(forms.ModelForm):
#     class Meta:
#         model = EmailCampaign
#         widgets = {
#             'id': forms.RadioSelect,
#         }
#         exclude = ['body', 'title']
