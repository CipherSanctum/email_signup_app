# Email sign up app / list for Django 2.x

Includes a Roman nummeral captcha app with vanilla javascript.

### PROGRAM CREATED BY:
Kevin / DiscoMushroom from PwnSauceDesigns.com

### PURPOSE:
Big companies have proven their ability to censor people based on their beliefs, including email list building companies. I created this program to cut out the middleman. Whether the beliefs of those in question are good or bad is not the point, and are also subjective. The point is that freedom of speech should be respected on a level playing ground for all. Not bestowing it for one and denying it for others, while also lying about what the banned person(s) said or did.

### FUTURE VERSIONS:
I will add the ability to have multiple EmailList model's, and the ability to send pretty html emails.

### LICENSE:
MIT License: https://choosealicense.com/licenses/mit/

### INSTRUCTIONS / USAGE:
For the latest version go to the blog for this at the following, or read below *(but I will update here too)*:
https://www.PwnSauceDesigns.com/blog/2018/8/15/beat-big-tech-censorship-by-making-your-own-email-list-cms/

1. Have your own VPS setup and running Django 2.x, and Python 3.x. It works on Django 2.0.5 and 2.1, but there are really not
that many huge changes with other versions of django. So check the code first if you're unsure.

2. Add the *email_signup_app/* folder to your projects root folder.

3. In settings.py, add *'email_signup_app.apps.EmailSignupAppConfig',* and *'captcha_app.apps.CaptchaAppConfig',* to
the INSTALLED_APPS list.

4. Add the values for *EMAIL_BACKEND, EMAIL_HOST*, *EMAIL_HOST_USER*, *EMAIL_HOST_PASSWORD*, *EMAIL_PORT*, and *EMAIL_USE_TLS* to your
*settings.py*. Documentation is at https://docs.djangoproject.com/en/2.0/ref/settings/#email-backend if you need more help.

5. Add *path('email_signup_app/', include('email_signup_app.urls', namespace='email_signup_app')),* to your projects urls.py.

6. In your root project's templates/ folder, add the admin/ folder into it. If you already have an admin/ folder there, just
add the app name folder inside that. This is necessary to override the default templates for the specific pages, so laymen can
get the instructions on how to use it properly.

7. Make sure the templates in email_signup_app/ are extending off whatever your base.html file is, with the proper block tags,
and edit any part of the templates content as you need. You will need to, because some of it has filler text.

8. Add my css styles to your css style sheet. Make sure none of them overlap with yours.

9. Make sure your DMARC, DKIM, SPF, etc. records are properly set on your VPS that's running Django, along with an
appropriate email for DMARC reports. Go to https://aritic.com/blog/aritic-mail/create-dmarc-record/ for an easy intro on how
to do that. You can also go to https://tools.ietf.org/html/rfc7489#section-6.3 for any deeper detail on info if you need it.

10. Go to Fail2Ban at https://www.fail2ban.org/wiki/index.php/Main_Page, scroll to it's documentation, read it,
and enable it on the server running Django to make it more secure. Do an internet search if you need more help with it.

11. *python manage.py makemigrations*

12. *python manage.py migrate*

13. *sudo systemctl restart gunicorn* (or whatever wsgi / distro of linux you're using to recognize the changes)

14. You will need to pip install Pillow, with any dependencies (haven't done it in awhile, but I think the only one was
psycopg2). Then upload the images from captcha_images/ into the Captcha App section on the admin panel, with the proper
Roman Numeral values.

15. Make an EmailCampaign instance.

16. Follow the directions in the EmailCampaign admin template for warming up your email server, and the directions on
the removal page when deleting from the list.

Enjoy!
