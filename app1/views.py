import os
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
import razorpay
from .models import Registeration,TaxiBooking,TaxiDetails,DriverRegisteration,TaxiDetailsHistory
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required


# Create your views here.

def Index(request):
    return render(request,'index.html')

def SignUp(request):
    if request.method=='POST':
        model=Registeration()
        model.name=request.POST['name']
        model.email=request.POST['email']
        model.mobile=request.POST['mobile']
        model.password=request.POST['password']
        model.country=request.POST['country']
        model.city=request.POST['city']
        model.pincode=request.POST['pincode']
        model.save()
        return redirect('signin')
    return render(request,'signup.html')

def DriverSignUp(request):
    if request.method=='POST':
        model=DriverRegisteration()
        model.name=request.POST['name']
        model.email=request.POST['email']
        model.mobile=request.POST['mobile']
        model.password=request.POST['password']
        model.badge_number=request.POST['badge_number']
        model.save()
        return redirect('driversignin')
    return render(request,'driversignup.html')


def SignIn(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        try:
            model=Registeration.objects.get(email=email)
            if model.password==password:
                request.session['email1']=email
                return redirect('search')
            else:
                return HttpResponse('Wrong credential')
        except:
            return HttpResponse('Unknow User')
    return render(request,'signin.html')

def DriverSignIn(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        try:
            model=DriverRegisteration.objects.get(email=email)
            if model.password==password:
                request.session['email']=email
                return redirect('driverapproval')
            else:
                return HttpResponse('Wrong credential')
        except:
            return HttpResponse('Unknow User')
    return render(request,'driversignin.html')

def DriverDetails(request):
   
    if 'email' in request.session.keys():
        try:
            driver= DriverRegisteration.objects.get(email=request.session['email'])
            taxi= TaxiDetails.objects.get(driver=driver)
            return render(request,'mydetails.html',{'driver':driver,'taxi':taxi})
        except:
                return HttpResponse('<h1>wait for admin add taxi for you</h1>')
    else:
        return redirect('driversignin')
   

def search(request):
    if 'email1' in request.session:
        user=Registeration.objects.get(email=request.session['email1'])
        print(user)
        if request.method=='POST':
            med = TaxiDetails.objects.all().filter(Q(source__icontains= request.POST['source']) | Q(destination__icontains = request.POST['destination']))
            data = {
                'med':med,
                'user':user
            }
            return render(request,'sear.html',data)
        else:
            med = TaxiDetails.objects.all()
            data = {
                'med':med,
                'user':user
            }
            return render(request,'sear.html',data)
    else:
        return redirect('signin')
        
def driverapproval(request):
    if 'email' in request.session.keys():
        try:
            driver=DriverRegisteration.objects.get(email=request.session['email'])
            taxi=TaxiDetails.objects.get(driver=driver,is_accepted=False)
            model=TaxiBooking.objects.filter(taxi=taxi)
            print(taxi)
            return render(request,'approval.html',{'model':model,'taxi':taxi})
        except:
            print('No taxi')
            return render(request,'approval.html')
    else:
        print('No user')
        return redirect('driversigin')

def driverbookingapproval(request,id):
    if 'email' in request.session.keys():
        driver=DriverRegisteration.objects.get(email=request.session['email'])
        model=TaxiBooking.objects.get(id=id)
        taxi_model=TaxiDetails.objects.get(driver=driver)
        if request.method=='POST':
            model.is_booked=True
            model.save()
            taxi_model.is_accepted=True
            taxi_model.save()
            driverhistory=TaxiDetailsHistory()
            driverhistory.user=model.user
            driverhistory.taxi=taxi_model
            driverhistory.driver=driver
            driverhistory.save()
            return redirect('driverapproval')
        return render(request,'driverbookingapproval.html',{'driver':driver,'model':model})
    else:
        return redirect('driversignin')
    
    
def taxibookingdetails(request,id):
    if 'email1' in request.session.keys():
        use_data=Registeration.objects.get(email=request.session['email1'])
        taxi=TaxiDetails.objects.get(id=id)
        taxibook=TaxiBooking()
        taxibook.user=use_data
        taxibook.taxi=taxi
        taxibook.save()
        taxi.is_booked=True
        taxi.save()
        return redirect('getbookingdetails')
    else:
        return redirect('signin')

def getbookeddetails(request):
    user=Registeration.objects.get(email=request.session['email1'])
    model=TaxiBooking.objects.filter(user=user)
    if request.POST:
        model1=TaxiDetails.objects.get(taxi_no=request.POST['taxi_no'])
        model1.is_booked=False
        model1.save()
        model2=TaxiBooking.objects.get(taxi=model1)
        model2.delete()
        return redirect('search')
    return render(request,'allbookingdetails.html',{'model':model,'user':user})

def canseltaxi(request,id):
    user=Registeration.objects.get(email=request.session['email1'])
    model=TaxiBooking.objects.filter(user=user)
    if request.POST:
        model1=TaxiDetails.objects.get(taxi_no=request.POST['taxi_no'])
        model1.is_booked=False
        model1.save()
        model.delete()

def myorder(request):
    if 'email1' in request.session.keys():
        try:
            user=Registeration.objects.get(email=request.session['email1'])
            taxi=TaxiBooking.objects.get(user=user,is_finished=False)
            taxi_details=TaxiDetails.objects.get(taxi_no=taxi.taxi)
            if request.method=='POST':
                taxi.is_finished=True
                taxi_details.is_booked=False
                taxi_details.is_accepted=False
                taxi_details.save()
                taxi.delete()
                return redirect('search')
            return render(request,'myorder.html',{'model':taxi,'user':user})
        except:
            return render(request,'myorder.html',{'model':'No data','user':user})
    else:
        return redirect('signinin')

def history(request):
    if 'email' in request.session.keys():
        driver=DriverRegisteration.objects.get(email=request.session['email'])
        taxi=TaxiDetailsHistory.objects.filter(driver=driver)
        return render(request,'history.html',{'model':taxi,'user':driver})
    else:
        return redirect('driversignin')
def logout(request):
    if 'email1' in request.session.keys():
        del request.session['email1']
        # print(request.session['email'])
        return redirect('signin')
    return redirect('signin')
        

def driverlogout(request):
    if 'email' in request.session.keys():
        del request.session['email']
        # print(request.session['email'])
        return redirect('driversignin')
    return redirect('driversignin')
        


def checkout(request,pk):
    if 'email1' in request.session.keys():
        user=Registeration.objects.get(email=request.session['email1'])
        razorpay_client = razorpay.Client(
            auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_SECRET_KEY"))
        )
        
        taxi_booking = TaxiBooking.objects.get(pk=pk)
        
        currency = 'INR'
        
        order_data = {
            'amount':int(taxi_booking.taxi.price) * 100,
            'currency':currency,
            'payment_capture':"0",
            'notes':{
                'pk':taxi_booking.pk
            }
        }
        razorpay_order = razorpay_client.order.create(
            order_data
        )

        # Prepare context for rendering
        context = {
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_merchant_key": os.getenv("RAZORPAY_KEY_ID"),
            "razorpay_amount": taxi_booking.taxi.price,
            "currency": currency,
            "callback_url": "/payment-success/",
            'user':user
        }
        return render(request, "razorpay_payment.html", context=context)
    else:
        return redirect('signinin')
        


@csrf_exempt
def payment_success(request):
    if 'email1' in request.session.keys():
        user=Registeration.objects.get(email=request.session['email1'])
        if request.method != "POST":
            return HttpResponseBadRequest()
        
        razorpay_client = razorpay.Client(
            auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_SECRET_KEY"))
        )

        payment_id = request.POST.get("razorpay_payment_id", "")
        razorpay_order_id = request.POST.get("razorpay_order_id", "")
        signature = request.POST.get("razorpay_signature", "")

        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }
        is_verified = razorpay_client.utility.verify_payment_signature(params_dict)
        if not is_verified:
            return HttpResponseBadRequest()
        
        order = razorpay_client.order.fetch(razorpay_order_id)
        pk = order.get('notes').get('pk')
        taxi_booking = get_object_or_404(TaxiBooking,pk=pk)

        try:
            razorpay_client.payment.capture(payment_id, float(taxi_booking.taxi.price)*100)
        except:
            return HttpResponseBadRequest()
        taxi_booking.is_paid = True
        taxi_booking.payment_id = payment_id
        taxi_booking.save()
        
        return render(request, "success_payment.html",{'user':user})
    else:
        return redirect('signinin')



