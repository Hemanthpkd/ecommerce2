from typing import Any
from django.db.models.query import QuerySet
# from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.views.generic import View,CreateView,FormView,ListView,DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator


# we want to create a decorator named signin_required so that when this decorator applied on the respective field ,
#  only logined user can open the page

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'invalid session..')
            return redirect('login')
        else:
            return fn(request,*args,**kwargs)
    return wrapper


class SignupView(CreateView):
    model=User
    form_class=RegisterForm
    template_name='register.html'
    success_url=reverse_lazy('login')
    success_message = "Your account was created successfully. Please log in."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"logged in seccessfully")
                return redirect("home")
            else:
                messages.error(request,"provided credentials are invalid")
                return render(request,"login.html",{"form":form})


# def HomeView(request):
#     return render(request,'index.html',{})

@method_decorator(signin_required,name='dispatch')
class HomeView(ListView):
    model=Products
    template_name='home.html'
    success_url=reverse_lazy('home')
    context_object_name='products'


@method_decorator(signin_required,name='dispatch')
class ProductDetailsView(DetailView):
    model=Products
    template_name='product-details.html'
    context_object_name='product'
    pk_url_kwarg='id'

@method_decorator(signin_required,name='dispatch')
class AddToCartView(View):

    def post(self,request,*args,**kwargs):
        qty=request.POST.get("qty")
        user=request.user
        id=kwargs.get("id")
        products=Products.objects.get(id=id)
        Carts.objects.create(product=products,user=user,qty=qty)
        return redirect('home')
    
@method_decorator(signin_required,name='dispatch')
class  CartListView(ListView):
    model=Carts
    template_name='cart-list.html'
    context_object_name='carts'
    def get_queryset(self):
        return Carts.objects.filter(status='in-cart')

@method_decorator(signin_required,name='dispatch')
class CartRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Carts.objects.filter(id=id).update(status="cancelled")
        return redirect('home')
    
@method_decorator(signin_required,name='dispatch')
class MakeOrderView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        cart=Carts.objects.get(id=id)
        return render(request,'checkout.html',{"cart":cart})
    
    def post(self,request,*args,**kwargs):
        user=request.user
        address=request.POST.get("address")
        id=kwargs.get("id")
        cart=Carts.objects.get(id=id)
        product=cart.product
        Orders.objects.create(product=product,user=user,address=address)
        cart.status='order-placed'
        cart.save()
        return redirect('home')

@method_decorator(signin_required,name='dispatch')
class MyOrderView(ListView):
    model=Orders
    template_name='order-list.html'
    context_object_name='order'
    def get_queryset(self):
        return Orders.objects.filter(status='order-placed')
    

@method_decorator(signin_required,name='dispatch')
class OrderRemoveView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        order = Orders.objects.get(id=id)
        if order.status == "order-placed":
            order.status = "cancelled"
            order.save()
        return redirect("order-list")
    
@method_decorator(signin_required,name='dispatch')
class OfferListView(ListView):
    model=Offers
    template_name='offers.html'
    context_object_name='offers'

@method_decorator(signin_required,name='dispatch')
class AddReviewView(View):
    def get(self,request,*args,**kwargs):
        form=ReviewForm()
        return render(request,'review.html',{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=ReviewForm(request.POST)
        id=kwargs.get("id")
        pro=Products.objects.get(id=id)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.product=pro
            form.save()
            return redirect('home')
        else:
            return render(request,'review.html',{"form":form})
        

def signout_view(request):
    logout(request)
    messages.success(request,"logout successfully..")
    return redirect("login")
    
    


