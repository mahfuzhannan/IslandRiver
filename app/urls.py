from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from app import views

rest_api_router = routers.DefaultRouter()
rest_api_router.register(r'users', views.RestApiUserViewSet)
rest_api_router.register(r'catalogs', views.RestApiCatalogViewSet)
rest_api_router.register(r'products', views.RestApiProductViewSet)
rest_api_router.register(r'categories', views.RestApiCatalogCategoryViewSet)
rest_api_router.register(r'baskets', views.RestApiBasketViewSet)
rest_api_router.register(r'baskets/products', views.RestApiBasketProductViewSet)
rest_api_router.register(r'orders', views.RestApiOrderViewSet)
rest_api_router.register(r'orders/products', views.RestApiOrderProductViewSet)
rest_api_router.register(r'reviews', views.RestApiReviewProductViewSet)


urlpatterns = [
    # signup page
    url(r'^signup/$', views.signup_user, name='signup'),
    # custom login
    url(r'^login/$', views.login_user, name='login'),
    # custom logout
    url(r'^logout/$', views.logout_user, name='logout'),
    # django auth change password
    url(r'^change-password/$', auth_views.password_change, {'template_name': 'app/password_change.html'}),
    # django auth change password done
    url(r'^password-change-done/$', auth_views.password_change_done, name='password_change_done'),

    # home page
    url(r'^$', views.home, name='home'),
    # about page
    url(r'^about/$', views.about, name='about'),
    # shop page
    url(r'^shop/(.*)/(.*)/$', views.shop_product, name='shop'),
    url(r'^shop/(.*)/$', views.shop, name='shop'),
    url(r'^shop/$', views.shop, name='shop'),
    # product review
    url(r'^products/review/$', views.product_review, name='review'),
    # account page
    url(r'^account/$', views.account_view, name='account'),
    # basket page
    url(r'^basket/$', views.basket_view, name='basket'),
    # handle basket stuff
    url(r'^baskets/$', views.baskets),
    # get basket products
    url(r'^baskets/products/$', views.BasketProductList.as_view()),
    # checkout
    url(r'^checkout/$', views.checkout),
    # order summary
    url(r'^orders/summary/$', views.order_summary_view),

    # rest_framework api, use this for all GET only
    url(r'^api/', include(rest_api_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


]