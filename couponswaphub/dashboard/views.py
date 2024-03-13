from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from coupon.models import Coupon
# Create your views here.

@login_required
def index(request):
    coupons=Coupon.objects.filter(published_by=request.user)

    return render(request,'dashboard/index.html',{
        'coupons':coupons,
    })

