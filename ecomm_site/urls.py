from django.contrib import admin
from django.urls import path, include
from . import  views 
from  django.conf import settings
from  django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name="base"),
    path('', views.index, name="index"),

    path('signup/',views.SignUp, name="signup"),
    path('accounts/', include('django.contrib.auth.urls')),
    
   path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),


     path('contact_us/', views.contact_page, name="contact_page"),


     path('checkout/', views.CheckOut, name="checkout"),

     path('order/', views.YourOrder, name="order"),
     path('product/', views.Product_Page, name="product"),

     path("product/<str:id>", views.Product_Detail, name="product_detail"),

     path('search/', views.Search, name="search"),



     path('recommendation/', views.outfit_recommendation, name='outfit_recommendation'),

] + static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)