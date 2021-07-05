from django.contrib import admin
from django.urls import path
from .views import Index,Login,Signup,logout,Cart,CheckOut,OrderView
from .middlewares.auth import auth_middleware

urlpatterns = [
    path('', Index.as_view(), name="homepage"),
    path('login', Login.as_view() , name = "login"),
    path('signup', Signup.as_view(), name="signuppage" ),
    path('logout',logout, name = "logout"),
    path('cart', Cart.as_view(), name="cartpage"),
    path('check-out', CheckOut.as_view(), name="checkoutpage"),
    # modification on 4 jul 10.36
    # path('check-out', auth_middleware(CheckOut.as_view()), name="checkoutpage"),
    path('orders', auth_middleware(OrderView.as_view()), name = "orders"),
]
