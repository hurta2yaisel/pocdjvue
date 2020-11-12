from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from oscar_vue_api.authtoken import obtain_auth_token
from oscar_vue_api import views, search
from oscarapi import urls

app_name = 'api'

urlpatterns = [
    path('user/login', obtain_auth_token),
    path('user/me', views.CurrentUserView.as_view()),
    path('cart/create', views.CreateBasketView.as_view()),
    path('cart/pull', views.PullBasketView.as_view()),
    path('cart/update', views.UpdateBasketItemView.as_view()),
    path('cart/delete', views.DeleteBasketItemView.as_view()),
    path('cart/totals', views.BasketTotalsView.as_view()),
    path('cart/shipping-information', views.BasketTotalsView.as_view()),
    # path('products/index', views.ProductList.as_view(), name='product-list'),
    re_path('catalog*', views.ElasticView.as_view()),
]  # + urls.urlpatterns

# print(urlpatterns)
