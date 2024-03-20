from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # CATEGORY
    path('list-category', views.category_list, name='category-list'),
    path('category-detail/<int:pk>/', views.category_detail, name='create-category'),
    path('', views.index, name='index'),

    # PRODUCTS
    path('products-list',views.product_list),
    path('products-detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('products-create', views.product_create, name='product_create'),
    path('products-delete/<int:pk>/', views.product_delete, name='product_delete'),

    # CART
    path('carts', views.carts, name='carts'),
    path('cart/', views.cart_list, name='cart_list'),
    path('cart-detail/<int:user_id>/', views.cart_detail, name='cart_det'),
    path('cart-add', views.cart_add, name='cart_add'),
    path('create-cart/<int:pk>/', views.create_cart, name = 'create_cart'),
    
    #ORDER 
    path('orders/', views.order_list, name='order_list'),
    path('create-order', views.create_order, name='creat_order'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('order-delete', views.order_delete, name='order_delete')
]