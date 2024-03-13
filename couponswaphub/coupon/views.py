from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from.forms import NewCouponForm,EditCouponForm
from .models import Category,Coupon
# Create your views here.


def coupons(request):
    query=request.GET.get('query','')
    category_id=request.GET.get('category',0)
    categories=Category.objects.all()
    coupons=Coupon.objects.filter(is_booked=False)

    if category_id:
        coupons=coupons.filter(category_id=category_id)

    if query:
        coupons=coupons.filter(Q(name__icontains=query) |Q(description__icontains=query) )
    return render(request,'coupon/coupons.html',{
        'coupons':coupons,
        'query':query,
        'categories':categories,
        'category_id':int(category_id)
    })
def detail(request,pk):
    coupon =get_object_or_404(Coupon,pk=pk)
    related_coupons=Coupon.objects.filter(category=coupon.category,is_booked=False).exclude(pk=pk)[0:3]

    return render(request,'coupon/detail.html',{
        'coupon':coupon,
        'related_coupons':related_coupons
    })

@login_required()
def new(request):
    if request.method=='POST':
        form=NewCouponForm(request.POST,request.FILES)

        if form.is_valid():
            coupon=form.save(commit=False)
            coupon.published_by=request.user
            coupon.save()

            return redirect('coupon:detail',pk=coupon.id)

    else:
       form=NewCouponForm()

    return render(request,'coupon/form.html',{
        'form':form,
        'title':'New coupon'
    })

@login_required()
def edit(request,pk):
    coupon=get_object_or_404(Coupon,pk=pk ,published_by=request.user)

    if request.method=='POST':
        form=EditCouponForm(request.POST,request.FILES,instance=coupon)

        if form.is_valid():
           form.save()

           return redirect('coupon:detail',pk=coupon.id)

    else:
       form=EditCouponForm(instance=coupon)

    return render(request,'coupon/form.html',{
        'form':form,
        'title':'Edit coupon'
    })


@login_required
def delete(request,pk):
    coupon=get_object_or_404(Coupon,pk=pk,published_by=request.user)
    coupon.delete()

    return redirect('dashboard:index')