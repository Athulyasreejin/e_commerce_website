from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.views import View
from django.contrib.auth import logout
from .models import Admin_Signup,Category,Product,Order,OrderItem
from user.models import Customer
from user.views import ViewOrderedItemsView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



# Create your views here.

def index(request):
    return render(request,'main/index.html')

def calendar(request):
    return render(request,'main/calendar.html')


def resetpassword(request):
    return render(request,'main/reset-password.html')

def tables(request):
    return render(request,'main/tables.html')

def add_category(request):
    return render(request,'main/category.html')




class AdminLoginView(View):
    def get(self, request):
        return render(request, 'main/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin_user = Admin_Signup.objects.get(username=username)
        except Admin_Signup.DoesNotExist:
            admin_user = None

        if admin_user and admin_user.password == password:
            request.session['name'] = admin_user.username
            request.session['id'] = admin_user.id
            return redirect('index')
        else:
            return render(request, 'main/login.html', {'error': "Invalid username or password"})

class AdminLogoutView(View):
    def get(self,request):
        your_data =request.session.get('id',None)
        if your_data is not None:
            del request.session['id']
        logout(request) 
        return redirect ('admin_login') 
     
class AddCategoryView(View):
    def get(self, request):
        return render(request, 'main/addcategory.html')

    def post(self, request):
        category_name = request.POST.get('category')
        if category_name:
            new_category = Category(name=category_name)
            new_category.save()
            return redirect('category_list')

        return render(request, 'main/addcategory.html')

class CategoriesListView(View):
    template_name = 'main/category_list.html'

    def get(self, request):
        categories = Category.objects.all().order_by('-id')
        return render(request, self.template_name, {'categories': categories})
class EditCategoryView(View):
    template_name = 'main/editcategory.html'

    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            return render(request, self.template_name, {'category': category})
        except Category.DoesNotExist:
            return redirect('category_list')

    def post(self, request, category_id):
        category_name = request.POST.get('category')
        try:
            category = Category.objects.get(id=category_id)
            if category_name:
                category.name = category_name
                category.save()
            return redirect('category_list')
        except Category.DoesNotExist:
            return redirect('category_list')

class DeleteCategoryView(View):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
        except Category.DoesNotExist:
            pass  # Handle the case where the category doesn't exist

        return redirect('category_list')



class AddProduct(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()  # Fetch all products
        return render(request, 'main/product.html', {'cat': categories, 'product': products})

    def post(self, request):
        if request.method == 'POST':
            product_name = request.POST['name']
            product_description = request.POST['description']
            product_category_id = request.POST['category']
            product_category = Category.objects.get(id=product_category_id)
            product_color = request.POST['color']
            product_size = request.POST['size']

            product_price = request.POST['price']
            product_count = request.POST['quantity']
            product_photo = request.FILES.get('image')
            new_product = Product(
                name=product_name,
                category=product_category,
                description=product_description,
                color=product_color,
                size=product_size,
                price=product_price,
                quantity=product_count,
                image=product_photo
            )
            new_product.save()
            print('success')
            
        categories = Category.objects.all()
        products = Product.objects.all()  # Fetch all products
        return render(request, 'main/product.html', {'cat': categories, 'product': products})

        
class ProductsPageView(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all().order_by('-id')
        context = {'cat': categories, 'product': products}
        return render(request, 'main/product.html',context)

class DeleteProductView(View):
    def get(self, request, p):
        prdct = Product.objects.get(id=p)
        prdct.delete()
        return redirect('products_page')

class EditProductPageView(View):
    def get(self, request, p):
        categories = Category.objects.all()
        prdct = Product.objects.get(id=p)
        return render(request, 'main/edit_product.html', {'product': prdct, 'category': categories})
    
    def post(self, request, p):
        categories = Category.objects.all()
        prdct = Product.objects.get(id=p)
        
        if request.method == 'POST':
            product_name = request.POST['name']
            product_description = request.POST['description']
            product_category_id = request.POST['category']
            product_category = Category.objects.get(id=product_category_id)
            product_color = request.POST['color']
            product_size = request.POST['size']

            product_price = request.POST['price']
            product_count = request.POST['quantity']
            product_photo = request.FILES.get('image')
            
            prdct.name = product_name
            prdct.category = product_category
            prdct.description = product_description
            prdct.color = product_color
            prdct.size = product_size

            prdct.price = product_price
            prdct.quantity = product_count
            
            if product_photo:
                prdct.image = product_photo
            
            prdct.save()
            
            return redirect('products_page')

        return render(request, 'main/edit_product.html', {'product': prdct, 'category': categories})

class CustomerListView(View):
    template_name = 'main/customer_list.html'  # Create this template

    def get(self, request):
        customers = Customer.objects.all()
        return render(request, self.template_name, {'customers': customers})

class OrderDetailsView(View):
    def get(self, request):
        orders = Order.objects.all()     
        order_items = OrderItem.objects.filter(order__in=orders)

        return render(request, 'main/order_details.html', {'order_items': order_items})



class UpdateStatusView(View):
    def post(self, request, *args, **kwargs):
        updated_orders = []  # To keep track of updated order IDs

        for key in request.POST.keys():
            if key.startswith('status_'):
                order_id = key[len('status_'):]
                new_status = request.POST[key]

                order_items = OrderItem.objects.filter(order_id=order_id)
                for order_item in order_items:
                    order = order_item.order
                    order.status = new_status
                    order.save()

                updated_orders.append(order_id)

        if updated_orders:
            # Add a success message for updated orders
            order_list = ', '.join(updated_orders)
            success_message = f"Status for order has been updated successfully."
            messages.success(request, success_message)

        return redirect('order_details')
