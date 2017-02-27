from django.conf.urls import url
from django.contrib.auth import views as auth_views
from app import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^signup/$', views.signup_page, name='signup'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^basket/$', views.basket, name='basket'),
    url(r'^setup/$', views.setup_shop, name='setup'),


    url(r'^items/$', views.get_items),

    url(r'^auth/signup/$', views.signup),
    url(r'^login/$', auth_views.login, {'template_name': 'app/login.html'}, name='login'),

]