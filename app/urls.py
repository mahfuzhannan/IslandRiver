from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),

    url(r'^shop/$', views.shop, name='shop'),

    url(r'^baskets/', views.baskets, name='baskets'),

    url(r'^items/$', views.get_items),
    url(r'^items/(?P<item_id>\d+)/$', views.get_item),

    url(r'^signup/$', views.signup_user, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
]