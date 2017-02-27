from django.conf.urls import url
from django.contrib.auth import views as auth_views
from app import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^basket/$', views.basket, name='basket'),


    url(r'^items/$', views.get_items),

    url(r'^signup/$', views.signup_user, name='signup'),
    url(r'^login/$', views.login_user, name='login'),

]