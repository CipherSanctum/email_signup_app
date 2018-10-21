from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


app_name = 'email_signup_app'


urlpatterns = [
    path('', cache_page(60*720)(views.email_signup_home), name='email_signup_home'),  # YourWebsite.com/email_signup/
    path('check_email/', cache_page(60*720)(views.email_signup_go_check), name='email_signup_go_check'),
    path('<int:unconf_email_id>/<uuid:random_uuid>/', cache_page(60*60)(views.email_signup_confirm), name='email_signup_confirm'),
    path('signup_done/<int:conf_email_id>/<uuid:random_uuid>/<int:rand_int>/download/', cache_page(60*60)(views.email_signup_done), name='email_signup_done'),

    # person adds self to removal list that can be removed by admin only:
    path('<int:conf_email_id>/<uuid:random_uuid>/remove/', views.email_list_remove, name='email_list_remove'),
    path('remove_done/', cache_page(60*720)(views.email_list_remove_done), name='email_list_remove_done'),
]
