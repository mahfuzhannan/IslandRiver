from django.conf.urls import url
from app import views

urlpatterns = [
    # static
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^account/', views.account_view, name='account'),
    url(r'^basket/', views.basket_view, name='basket'),
    # auth
    url(r'^signup/$', views.signup_user, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),

    # REST
    url(r'^items/', views.items),
    # url(r'^items/(?P<item_id>\d+)/$', views.items),
    url(r'^baskets/', views.items),
    url(r'^users/', views.items),
]