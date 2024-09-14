from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view),
    path('about-us/', views.about_us_view),
    path('shop-rules/', views.shop_rules),
    path('product-category/<str:cat>/', views.category_product_view, name='category_product'),
    path('serach/', views.serach_view, name='serach-empty'),
    path('serach/<str:serach_text>', views.serach_view, name='serach-empty'),
    path('shop/', views.shop_view, name='shop-empty'),
    path('product/<int:product_id>/', views.product_view, name='product'),
    path('blog/', views.blog_view, name='blog-empty'),
    path('site-ajax/', views.ajaxs, name='ajax'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('my-account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('category/<str:cat>/', views.category_blog_view, name='category_blog'),
    path('404/', views.page_not_found, name='page_not_found'),
    path('<str:blog_title>/', views.blog_view, name='blog'),
]
