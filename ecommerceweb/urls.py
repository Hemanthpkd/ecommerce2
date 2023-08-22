from django.contrib import admin
from django.urls import path
from ecommerceweb import views


urlpatterns = [
    # path("",views.store,name='store'),
    # path("cart/",views.cart,name='cart'),
    # path("checkout/",views.checkout,name='checkout'),
    path('register/',views.SignupView.as_view(),name='register'),
    path("login/",views.LoginView.as_view(),name='login'),
    path("",views.HomeView.as_view(),name='home'),
    path("product_details/<int:id>/",views.ProductDetailsView.as_view(),name='product_details'),
    path('products/<int:id>/carts/add',views.AddToCartView.as_view(),name='cart-add'),
    path('products/carts/all',views.CartListView.as_view(),name='cart-list'),
    path("products/<int:id>/cart-change",views.CartRemoveView.as_view(),name='cart-change'),
    path('orders/add/<int:id>',views.MakeOrderView.as_view(),name='make-order'),
    path('orders/list',views.MyOrderView.as_view(),name='order-list'),
    path("order/<int:id>/remove",views.OrderRemoveView.as_view(),name="order-remove"),
    path('offers',views.OfferListView.as_view(),name='offers'),
    path('reviews/<int:id>',views.AddReviewView.as_view(),name='add-review'),
    path('logout/',views.signout_view,name='signout')
]
