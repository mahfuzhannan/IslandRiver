from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^basket/$', views.basket, name='basket'),
    url(r'^setup/$', views.setup_shop, name='setup'),


    url(r'^items/$', views.get_items),
]