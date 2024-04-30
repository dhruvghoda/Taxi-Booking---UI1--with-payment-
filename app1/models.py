from django.db import models

# Create your models here.
class Registeration(models.Model):
    name=models.CharField(max_length=30,null=True)
    mobile=models.CharField(max_length=30,null=True)
    email=models.EmailField()
    password=models.CharField(max_length=30,null=True)
    city=models.CharField(max_length=40,null=True)
    country=models.CharField(max_length=40,null=True)
    pincode=models.CharField(max_length=30,null=True)

    def __str__(self) -> str:
        return self.email

class DriverRegisteration(models.Model):
    name=models.CharField(max_length=30,null=True)
    mobile=models.CharField(max_length=30,null=True)
    email=models.EmailField()
    password=models.CharField(max_length=30,null=True)
    badge_number=models.CharField(max_length=20,unique=True,null=True)

    def __str__(self) -> str:
        return self.email



class TaxiDetails(models.Model):
    taxi_no=models.CharField(max_length=15,null=True)
    driver=models.ForeignKey(DriverRegisteration,on_delete=models.CASCADE)
    source=models.CharField(max_length=40,null=True)
    destination=models.CharField(max_length=40,null=True)
    price=models.IntegerField(null=True)
    is_booked=models.BooleanField(default=False)
    is_accepted=models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.taxi_no

class TaxiBooking(models.Model):
    user=models.ForeignKey(Registeration,null=True,on_delete=models.CASCADE)
    taxi=models.ForeignKey(TaxiDetails,null=True,on_delete=models.CASCADE)
    booked_time=models.DateField(null=True,auto_now_add=True)
    is_booked=models.BooleanField(default=False)
    is_finished=models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100)
    


class TaxiDetailsHistory(models.Model):
    driver=models.ForeignKey(DriverRegisteration,on_delete=models.CASCADE)
    taxi=models.ForeignKey(TaxiDetails,on_delete=models.CASCADE)
    user=models.ForeignKey(Registeration,on_delete=models.CASCADE)
    booked=models.DateField(auto_now_add=True)





