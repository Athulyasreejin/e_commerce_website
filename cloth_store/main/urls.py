from django.urls import path
from . import views 
from user.views import ViewOrderedItemsView

from .views import AdminLoginView,AdminLogoutView,AddCategoryView,AddProduct,ProductsPageView,DeleteProductView,EditProductPageView,CategoriesListView,DeleteCategoryView,EditCategoryView,CustomerListView,OrderDetailsView,UpdateStatusView
urlpatterns = [
    
    path('index', views.index, name='index'), 
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('', AdminLoginView.as_view(), name='admin_login'),
    path('reset-password', views.resetpassword, name='reset-password'), 
    path('tables', views.tables, name='tables'), 
    path('logout',AdminLogoutView.as_view(),name="logout"),
    path('products_page/', ProductsPageView.as_view(), name='products_page'),
    path('category_list/', CategoriesListView.as_view(), name='category_list'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('delete_category/<int:category_id>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('edit_category/<int:category_id>/', EditCategoryView.as_view(), name='edit_category'),

    # path('add_color/',AddColorView.as_view(), name='add_color'),
    # path('add_size/',AddSizeView.as_view(), name='add_size'),
    path('add_product/',AddProduct.as_view(), name='add_product'),

    path('delete_product/<int:p>/', DeleteProductView.as_view(), name='delete_product'),
    path('edit_product_page/<int:p>/', EditProductPageView.as_view(), name='edit_product_page'),
    path('order-details/', OrderDetailsView.as_view(), name='order_details'),
    path('update-status/', UpdateStatusView.as_view(), name='update_status'),


]