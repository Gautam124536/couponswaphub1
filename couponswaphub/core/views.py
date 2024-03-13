from django.shortcuts import render,redirect

from coupon.models import Category,Coupon

from .forms import SignupForm

def index(request):
    coupons=Coupon.objects.filter(is_booked=False)[0:6]
    categories=Category.objects.all()

    return render(request,'core/index.html',{
        'categories':categories,
        'coupons':coupons,
    })

def contact(request):
    return render(request,'core/contact.html')

def signup(request):
    if request.method=='POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')

    else:
        form = SignupForm()


    return render(request,'core/signup.html', {
        'form':form
    })