import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import City, Country, Language

# import mysql.connector as sql
# fn = ""
# ln = ""
# gn = ""
# em = ""
# pn = ""

# # Create your views here.

def send_otp(mobile, otp):     
    client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
    message = client.messages.create(body=f'your otp is:{otp}',from_=f'{settings.TWILIO_PHONE_NUMBER}',to=f'{settings.COUNTRY_CODE}{mobile}')
    return None    


def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()

        if check_user or check_profile:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'register.html', context)

        user = User(first_name=firstName, last_name=lastName, email=email)
        user.save()

        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('http://localhost:8000/otp/')

    return render(request, 'register.html')


def loginaction(request):
    return render(request, 'login_page.html')

@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        # Retrieve the data from the request
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')

        # Authenticate the user
        user = authenticate(request, mobile=mobile, otp=otp)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid email or OTP'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

@csrf_exempt
def otpVerify(request):
    mobile = request.session['mobile']
    if request.method=="POST":
        profile=Profile.objects.get(mobile=mobile)     
        if request.COOKIES.get('can_otp_enter')!=None:
            if(profile.otp==request.POST['otp']):
                red=redirect("home")
                red.set_cookie('verified',True)
                return red
            return HttpResponse("wrong otp")
        return HttpResponse("10 minutes passed")        
    return render(request,"otp.html",{'mobile':mobile})



@csrf_exempt
def logout_api(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def logout_view(request):
    logout(request)
    return redirect('http://localhost:8000/login/')




def country(request, code):
    country = get_object_or_404(Country, code=code)
    context = {'country': country}
    return render(request, 'country.html', context)




def search(request):
    query = request.GET.get('q')
    if query:
        cities = City.objects.filter(Q(name__icontains=query) | Q(country__name__icontains=query))
        countries = Country.objects.filter(name__icontains=query)
        languages = Language.objects.filter(name__icontains=query)
        context = {'query': query, 'cities': cities, 'countries': countries, 'languages': languages}
    else:
        context = {}
    return render(request, 'search.html', context)

# def signaction(request):
#     global fn, ln, gn, em, pn
#     if request.method=="POST":
#         m = sql.connect(host="localhost",user="root",passwd="1234",database="website")
#         cursor=m.cursor()
#         d=request.POST
#         for key,value in d.items():
#             if key=="first_name":
#                 fn=value
#             if key=="last_name":
#                 ln=value
#             if key=="gender":
#                 gn=value
#             if key=="email":
#                 em=value
#             if key=="mobile":
#                 pn=value
#         c="insert into users Values('{}','{}','{}','{}','{}')".format(fn,ln,gn,em,pn)
#         cursor.execute(c)
#         m.commit()

    # return render(request, "register.html")
