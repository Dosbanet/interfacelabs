from django.urls import include, path

from . import views

urlpatterns = [
    path('details/<int:merch_id>/', views.detail, name='detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cart/', views.cart, name='cart'),
    path('register/', views.Reg.as_view(), name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('purchase/', views.purchase, name='purchase'),
    path('', views.index, name='index'),
    path('cl_index/', views.cl_index),
    path('cl_login/', views.cl_login),
    path('cl_cart/', views.cl_cart),
    path('cl_reg/', views.cl_reg),
    path('cl_check/', views.cl_check),
]