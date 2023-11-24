from django.urls import path
from . import views
from .views import IndexView,ShopView,ProductDetailsView,SearchProductsView,SignUpView,UserLoginView,UserLogoutView,CartPageView,AddToCartView,ProfileView,ProfileEditView,ChangePasswordView,RemoveFromCartView,ClearCartView,ProductsByCategoryView, OrderNowView, ViewOrderedItemsView,CartOrderNowView
urlpatterns = [
    path('', IndexView.as_view(), name='index1'),
    path('shop', ShopView.as_view(), name='shop'),
    # path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('product/<int:product_id>/', ProductDetailsView.as_view(), name='product_details'),
    path('registration_page',SignUpView.as_view(),name='signup'),
    path('signin', UserLoginView.as_view(), name="signin"),

    path('userlogout/', UserLogoutView.as_view(), name='logout'),
    path('userprofile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    path('search',SearchProductsView.as_view(),name='search_products'),
    path('cart/', CartPageView.as_view(), name='cart'),
    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('clear_cart/', ClearCartView.as_view(), name='clear_cart'),
    path('products/category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('order/<int:product_id>/', OrderNowView.as_view(), name='order_now'),
    path('cart_order_now/',CartOrderNowView.as_view() , name='cart_order_now'),
    path('view_ordered_items/',ViewOrderedItemsView.as_view(), name='view_ordered_items'),

]
