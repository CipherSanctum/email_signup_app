from django.urls import path
from . import views
# from django.views.decorators.cache import cache_page


app_name = 'email_signup_app'


urlpatterns = [
    path('', views.email_signup_home, name='email_signup_home'),
    path('<int:unconf_email_id>/<uuid:random_uuid>/', views.email_signup_confirm, name='email_signup_confirm'),
    path('<int:conf_email_id>/<uuid:random_uuid>/unsubscribe/', views.email_unsubscribe, name='email_unsubscribe'),
]
