from django.shortcuts import render,redirect
from SiteAdm.models import *
from Guest.models import *
from User.models import *
from SiteAdm.views import *
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.hashers import make_password, check_password


def Logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    if 'admid' in request.session:
        del request.session['admid']
    return redirect('Guest:Login')

def Login(request):
    if request.method == "POST":
        email=request.POST.get("txtemail")
        password=request.POST.get("txtpassword")
        admincount=tbl_admin.objects.filter(admin_email=email).count()
        usercount=tbl_user.objects.filter(user_email=email).count()

        if usercount>0:
            user = tbl_user.objects.filter(user_email=email).first()  # Get the user object
            if user:
                print(f"Found user: {user.user_email}")
            if user and check_password(password, user.user_password):  # Verify the password
                if user.user_status==1:
                    return render(request,"Guest/Login.html",{'msg':"Your Account is not Active"})
                else:
                    request.session['uid']=user.id
                    return redirect('User:HomePage')
            else:
                return render(request, "Guest/Login.html", {'msg': "Invalid Email or Password"})
        elif admincount>0:
            admin = tbl_admin.objects.get(admin_email=email)
            if check_password(password, admin.admin_password):  # Verify the password
                request.session['admid'] = admin.id
                return redirect('SiteAdm:HomePage')
            else:
                return render(request, "Guest/Login.html", {'msg': "Invalid Email or Password"})
    else:
        return render(request,"Guest/Login.html")

def UserRegistration(request):
    data=tbl_user.objects.all()
    if request.method =="POST":
        uname=request.POST.get("txtname")
        uemail=request.POST.get("txtemail")
        ucontact=request.POST.get("txtcontactno") 
        lat=request.POST.get("latitude")
        long=request.POST.get("longitude")
        uphoto=request.FILES.get("fphoto")
        uproof=request.FILES.get("fproof")
        upass = make_password(request.POST.get("txtpassword")) # Encrypt the password
        if uemail in tbl_user.objects.values_list('user_email', flat=True):
            return render(request, "Guest/UserRegistration.html", {'msg': "Email already exists", "udata": data})
        if tbl_user.objects.filter(user_name=uname).exists():
            return render(request, "Guest/UserRegistration.html", {'msg': "Username already exists", "udata": data})
        tbl_user.objects.create(user_name=uname,user_email=uemail,user_contact=ucontact,user_latitude=lat,user_longitude=long,user_photo=uphoto,user_proof=uproof,user_password=upass)
        return redirect('Guest:Login')
    else:

        return render(request,"Guest/UserRegistration.html",{"udata":data})