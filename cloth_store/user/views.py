from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import logout,login
from django.views import View
from django.urls import reverse
from .forms import *
from django.contrib import messages

from main.models import Product,Category,Order,OrderItem
from .forms import ProductSearchForm
from django.contrib.auth.models import User
from .models import Customer,Cart,CartItem
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth
from django.contrib.auth.hashers import check_password





# Create your views here.


class IndexView(View):
    def get(self, request):
        Categories=Category.objects.all()
        products = Product.objects.all()
        return render(request, 'user/index1.html', {'products': products,'categories':Categories})

class ShopView(View):
    def get(self, request):
        Categories=Category.objects.all()

        products = Product.objects.all()
        return render(request, 'user/shop.html', {'products': products,'categories':Categories})


def about(request):
    Categories=Category.objects.all()

    return render(request,'user/about.html',{'categories':Categories})

def cart(request):
    return render(request,'user/cart.html')

def checkout(request):
    return render(request,'user/checkout.html')

class ProductDetailsView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Categories=Category.objects.all()

        context = {'product': product,'categories':Categories}
        return render(request, 'user/product_des.html', context)
    
class SearchProductsView(View):
    template_name = 'user/search_results.html'
    
    def get(self, request):
        form = ProductSearchForm(request.GET)
        query = None
        results = []
        Categories=Category.objects.all()


        if form.is_valid():
            query = form.cleaned_data['search_query']
            results = Product.objects.filter(name__icontains=query)
            
        context = {'form': form, 'query': query, 'results': results,'categories':Categories}
        return render(request, self.template_name, context)

class SignUpView(View):
    template_name = 'user/signup.html'


    def get(self, request):
        return render(request, self.template_name)


    def post(self, request):
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            mobile = request.POST['mobile']
            address = request.POST['address']
            user_name = request.POST['username']
            password = request.POST['password']

            if User.objects.filter(username=user_name).exists():
                msg = 'Sorry, the username already exists...'
                return render(request, self.template_name, {
                    'msg': msg,
                    'name': name,
                    'email': email,
                    'mobile': mobile,
                    'address': address,
                    'username': user_name
                })
            else:
                user = User.objects.create_user(
                    first_name=name,
                    email=email,
                    username=user_name,
                    password=password,
                )

                new_customer = Customer(user=user, mobile=mobile, address=address, name=name, email=email) 
                new_customer.save()
                return redirect('signin')
        Categories=Category.objects.all()

        return render(request, self.template_name,{'categories':Categories})

class UserLoginView(View):

    def get(self, request):
        Categories=Category.objects.all()

        return render(request, 'user/signin.html',{'categories':Categories})

    def post(self, request):
        if request.method == 'POST':
            user_name = request.POST['user_name']
            pass_word = request.POST['pass_word']
            user = auth.authenticate(username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                print('Success')
                return redirect('index1')
            else:
                print('Failed')
                return redirect('signin')     
                
                
class UserLogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('index1')


class CartPageView(View):
    template_name = 'user/cart.html'
    
    def get(self, request):
        current_user = request.user
        quantity = request.GET.get('quantity', None)
        Categories=Category.objects.all()

        try:
            cart = Cart.objects.get(user=current_user)
            cart_items = cart.items.all()
            total = sum(c.total() for c in cart_items)
            
            context = {'cart_items': cart_items, 'total': total, 'quantity': quantity,'categories':Categories}
            return render(request, self.template_name, context)
        except Cart.DoesNotExist:
            return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def get(self, request, product_id):
        return self.handle_add_to_cart(request, product_id)

    
    def post(self, request, product_id):
        return self.handle_add_to_cart(request, product_id)

    
    def handle_add_to_cart(self, request, product_id):
        current_user = request.user
        item = get_object_or_404(Product, id=product_id)
        qty = 1
        
        try:
            user_cart = Cart.objects.get(user=current_user)
            cart_item = user_cart.items.filter(item=item).first()

            if cart_item:
                new_total_quantity = cart_item.quantity + qty
                # Check if the new total quantity exceeds the available stock
                if new_total_quantity > item.quantity:
                    messages.error(request, "Sorry, It seems like requested quantity is more than available stock!")
                    return redirect('shop')
                
                cart_item.quantity = new_total_quantity
                cart_item.price = item.price * new_total_quantity
                cart_item.save()
            else:
                new_cart_item = CartItem(item=item, quantity=qty, price=item.price)
                new_cart_item.save()
                user_cart.items.add(new_cart_item)
                cart_item = new_cart_item
            Categories=Category.objects.all()

            return redirect(reverse('cart') + f'?quantity={cart_item.quantity}',{'categories':Categories})

        except Cart.DoesNotExist:
            user_cart = Cart(user=current_user)
            user_cart.save()
            new_cart_item = CartItem(item=item, quantity=qty, price=item.price)
            new_cart_item.save()
            user_cart.items.add(new_cart_item)
            return redirect(reverse('cart') + f'?quantity={qty}')

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_details = request.user.customer
        Categories=Category.objects.all()

        return render(request, 'user/profile.html', {'user_details': user_details,'categories':Categories})

class ProfileEditView(View):
    template_name = 'user/profile_edit.html'

    def get(self, request):
        user_details = request.user.customer
        Categories=Category.objects.all()

        return render(request, self.template_name, {'user_details': user_details,'categories':Categories})

    def post(self, request):
        user_details = request.user.customer

        user_details.name = request.POST['name']
        user_details.mobile = request.POST['mobile']
        user_details.email = request.POST['email']
        user_details.address = request.POST['address']
        user_details.save()

        return redirect('profile')


class ChangePasswordView(View):
    template_name = 'user/change_password.html'

    def get(self, request):
        form = ChangePasswordForm()
        Categories=Category.objects.all()

        return render(request, self.template_name, {'form': form,'categories':Categories})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)  
            return redirect('profile')

        return render(request, self.template_name, {'form': form})

class RemoveFromCartView(View):
    def get(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        cart = Cart.objects.get(user=request.user)
        if cart_item in cart.items.all():
            cart.items.remove(cart_item)
        return redirect('cart')

class ClearCartView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        cart.items.clear()
        return redirect('cart')

class ProductsByCategoryView(View):

    def get(self, request, category_id, *args, **kwargs):
        try:
            selected_category = get_object_or_404(Category, pk=category_id)
            products_in_selected_category = Product.objects.filter(category=selected_category)
        except Category.DoesNotExist:
            return render(request, self.template_name, {'categories': Category.objects.all()})

        categories = Category.objects.all()  
        
        context = {
            'selected_category': selected_category,
            'products': products_in_selected_category,
            'categories': categories,  
        }
        return render(request, 'user/products_by_category.html', context)

class CartOrderNowView(View):
    template_name = 'user/cart_order_now.html'
    @method_decorator(login_required, name='dispatch')

    def get(self, request):
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        total_price = sum(item.total() for item in cart_items)
        Categories = Category.objects.all()  
        
        context = {'cart_items': cart_items, 'total_price': total_price,'categories':Categories}
        return render(request, self.template_name, context)
    
    def post(self, request):
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        total_price = sum(item.total() for item in cart_items)
        
        # Check if any cart item quantity is out of stock
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.item.quantity:
                cart_item.quantity = cart_item.item.quantity
                cart_item.save()
        
        # Filter out cart items with a quantity of zero
        cart_items = cart_items.exclude(quantity=0)
        
        # Create the order and order items for the cart items
        order = Order.objects.create(user=request.user, total_price=total_price)
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order, 
                product=cart_item.item, 
                quantity=cart_item.quantity, 
                item_price=cart_item.item.price * cart_item.quantity
            )
            
            # Decrease the product quantity by the ordered quantity
            cart_item.item.quantity -= cart_item.quantity
            cart_item.item.save()
        
        # Mark cart items as ordered
        cart_items.update(is_ordered=True)
        
        # Clear the user's cart by deleting cart items
        cart_items.delete()
        
        return redirect('view_ordered_items')  # Redirect to the orders page

class OrderNowView(View):
    template_name = 'user/order_now.html'
    
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Categories = Category.objects.all()  

        context = {'product': product, 'default_quantity': 1,'categories':Categories}
        return render(request, self.template_name, context)
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        # Create a new order for the user
        order = Order.objects.create(user=request.user, total_price=product.price)

        # Create an order item for the product
        OrderItem.objects.create(order=order, product=product, quantity=1, item_price=product.price)

        # Decrease the product quantity by 1
        product.quantity -= 1
        product.save()

        return redirect('view_ordered_items')  # Redirect to the orders page
    
class ViewOrderedItemsView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        order_items = OrderItem.objects.filter(order__in=orders)
        Categories = Category.objects.all()  

        return render(request, 'user/order.html', {'order_items': order_items,'categories':Categories})
