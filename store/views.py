from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import  View
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator



# Create your views here.
class Index(View):
    def post(self, request):
        product = request.POST.get('product')#getting data product_id from index page
        cart = request.session.get('cart')#creating cart and adding quantities to respective product.
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] =1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        # print('cart', cart )
        # print(product)
        return  redirect("homepage")
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None # get products info from Product model.
        categories = Category.get_all_categories()#get all categories info
        categoryId = request.GET.get('category')
        if categoryId:
            products = Product.get_all_products_by_categoryid(categoryId)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        print('you are:', request.session.get('email'))#use of session to identify user.
        return render(request,'index.html',data)
        # return HttpResponse("hello")

# signup class
class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')
    def post(self, request):
        postdata = request.POST
        first_name = postdata.get('firstname')
        last_name = postdata.get('lastname')
        phone = postdata.get('phone')
        email = postdata.get('email')
        password = postdata.get('password')
        # value is created to store the data entered after error occured,
        value = {
            'first_name' : first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email
        }
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)
        # Saving
        # print(first_name,last_name,phone,email,password)
        if not error_message:
            # hash password before storing it in table using make_password method;
            customer.password = make_password(customer.password)
            customer.register()#save data of customer
            return redirect('homepage')#after saving customer data return to homepage
        else:
            # data variable hold error and values variabel which corresponds to error_message,
            # and value , these data are provided to signup page using data variable.
            data = {
                'error':error_message,
                'values':value
            }
            return render(request,"signup.html",data)

    def validateCustomer(self,customer):
        error_message = None
        if not customer.first_name:
            error_message = "First Name required!"
        elif len(customer.first_name) < 2:
            error_message = "First Name should be greater than 1 character"
        elif not customer.last_name:
            error_message = "Last Name Required!"
        elif len(customer.last_name) < 2:
            error_message = "Last Name should be greater than 2 character"
        elif not customer.phone:
            error_message = "Phone Number Required!"
        elif len(customer.phone) < 10:
            error_message = "Phone Number must be 10 digits."
        elif not customer.email:
            error_message = "Please Enter Email-address"
        elif not customer.password:
            error_message = "Please Enter a strong Password"
        elif len(customer.password) < 8:
            error_message = "Password must be at least 8 characters"
        elif customer.isExists():  # here we have checked whether the user with same email exists or not,
            # we have used customer variable and isExists method from Customer model/table.
            error_message = "Email address is already registered!!!"
        return error_message


# validation of customer(error handling):

# def registerUser(request):
#
# def signup(request):
#     if request.method=="GET":
#     else:
#         return registerUser(request)#if method of form is post registerUser is called.


# class Login
class Login(View):
    return_url = None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return  render(request, 'login.html')
    def post(self,request):
        name = None
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email_id(email)#customer variable holds object from method passed to Customer table
        error_message = None
        if customer:
            flag = check_password(password,customer.password)
            if flag:
                request.session['customer'] = customer.id#use of session to identify user id
                request.session['firstname'] = customer.first_name
                # print(customer.first_name)
                # request.session['customer_id'] = customer.id#use of session to identify user id
                request.session['email'] = customer.email#use of session to identify user email
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')

            else:
                error_message = 'Email or Password is Incorrect!!'
        else:
            error_message = 'Email or Password is Incorrect!!'
        # print(customer)
        # print(email,password)
        return render(request, 'login.html',{'error': error_message})

def logout(request):
    request.session.clear()
    return redirect("login")

class Cart(View):
    def get(self,request):
        try:
            ids = (list(request.session.get('cart').keys()))
            products = Product.get_products_by_id(ids)
            print(products)
            return render(request, 'cart.html',{'products':products})
        except:
            return HttpResponse("Cart is Empty")

class CheckOut(View):
    def post(self,request):
        # print(request.POST)
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))        
        if customer is None:
            return redirect('login')
        for product in products:
            order = Order(customer = Customer(id = customer),
                          product = product,
                          price = product.price,
                          address = address,
                          phone = phone,
                          quantity = cart.get(str(product.id))
                          )
            order.save()
            request.session['cart'] = {}
        print(address,phone,customer)
        print(order)
        return redirect("cartpage")

class OrderView(View):
    # @method_decorator(auth_middleware)
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request,'orders.html',{'orders': orders})

# def login(request):
#     if request.method=='GET':
#     elif request.method=='POST':


