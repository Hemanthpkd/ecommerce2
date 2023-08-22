from .models import Carts

def cart_count(request):
    if request.user.is_authenticated:
        Cnt=Carts.objects.filter(user=request.user,status="in-cart").count()
    else:
        Cnt=0
    return {"count":Cnt}