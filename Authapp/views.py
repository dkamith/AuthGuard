from django.shortcuts import render,redirect
from .forms import SignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login,authenticate,logout
from .utils import generate_otp_secret,generate_qr_code,get_totp
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
 

# Create your views here.
from django_ratelimit.exceptions import Ratelimited
from django.shortcuts import render
User=get_user_model()

def too_many_requests(request, exception):
    # return render(
    #     request,
    #     "verify_otp.html",
    #     {
    #         "rate_limited": True,
    #         "error": "Too many OTP attempts. Please wait 1 minute."
    #     },
    #     status=429
    # )
    retry_after = request.META.get('HTTP_RETRY_AFTER', 'a short while')
    
    context = {
        'message': "You've hit our rate limit. Please try again after " + retry_after + ".",
        'retry_after': retry_after,  
    }
    return render(request, '429.html', context, status=429)

def signupPage(request):
    if request.method=='POST':
        form =SignupForm(request.POST)
        if form.is_valid():
            user=User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            login(request,user)
            return redirect('enable2fA')
    else:
        form=SignupForm()
    return render(request,'signup.html',{'form':form})
def loginuser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect("enable2fA")
        else:
            return render(request,'login.html',{'error':'invalid password/username'})
    return render(request,'login.html')
        
@login_required
def enable2fA(request):
    user=request.user
    if user.is_2fa_enabled:
        return redirect("verifyotp")
    if not user.otp_secret:
        user.otp_secret=generate_otp_secret()
        user.save()
    qr_code=generate_qr_code(user.username,user.otp_secret)
    return render(request,"enable_2fa.html",{"qr_code":qr_code})
@login_required
@ratelimit(key='user_or_ip',rate='5/m',block=True)
def verifyotp(request):
    # if getattr(request, 'limited', False):
    #     return render(
    #         request,
    #         "verify_otp.html",
    #         {
    #             "rate_limited": True,
    #             "error": "Too many OTP attempts. Please wait 1 minute and try again."
    #         },
    #         status=429
    #     )
    if request.method=='POST':
        otp=request.POST.get("otp")
        totp=get_totp(request.user.otp_secret)

        if totp.verify(otp):
            request.user.is_2fa_enabled=True
            request.user.save()
            request.session["2fa_verified"]=True
            return redirect("dashboard")
        return render(request,"verify_otp.html",{"error":"invalid otp"})
    return render(request,"verify_otp.html")

@login_required
def dashboardpage(request):
    return render(request,'dashboard.html')

def logout_user(request):
    logout(request)
    request.session.flush()
    return redirect('login')



