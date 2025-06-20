from django.shortcuts import render,redirect
from SiteAdm.models import *
from User.models import *
from Guest.views import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from geopy.geocoders import Nominatim

def HomePage(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    return render(request,"SiteAdm/HomePage.html")

def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="ToolShareApp", timeout=12)
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address

def Category(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    catdata=tbl_category.objects.all()
    if request.method == "POST":
        catname = request.POST.get("cname")
        tbl_category.objects.create(category_name=catname)
        return redirect('SiteAdm:Category')
    else:
        return render(request,"SiteAdm/Category.html",{"cat":catdata})

def deletecat(request,did):
    tbl_category.objects.get(id=did).delete()
    return redirect('SiteAdm:Category')

def editcat(request,eid):
    data=tbl_category.objects.get(id=eid)
    if request.method=='POST':
        categoryname=request.POST.get("cname")
        data.category_name=categoryname
        data.save()
        return redirect('SiteAdm:Category')       
    else:
        return render(request,"SiteAdm/Category.html",{"cated":data})


def AdminRegistration(request):
    admindata=tbl_admin.objects.all()
    if request.method == "POST":
        adminname = request.POST.get("admname")
        adminemail = request.POST.get("admemail")
        adminpassword = make_password(request.POST.get("admpassword")) # Encrypt the password
        tbl_admin.objects.create(admin_name=adminname,admin_email=adminemail,admin_password=adminpassword)
        return redirect('Guest:Login')
    else:
        return render(request,"SiteAdm/AdminRegistration.html", {"admindata":admindata})
        
def deleteadmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return redirect('SiteAdm:AdminRegistration')

def editadmin(request,eid):
    data=tbl_admin.objects.get(id=eid)
    if request.method=='POST':
        adminname=request.POST.get("admname")
        adminemail=request.POST.get("admemail")
        adminpassword=request.POST.get("admpassword")
        data.admin_name=adminname
        data.admin_email=adminemail
        data.admin_password=adminpassword
        data.save()
        return redirect('SiteAdm:AdminRegistration')       
    else:
        return render(request,"SiteAdm/AdminRegistration.html",{"admed":data})


def Viewcomplaint(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_complaint.objects.all()
    if request.method=='POST':
        return redirect('SiteAdm:Reply')
    else:
        return render(request,"SiteAdm/Viewcomplaint.html",{"comp":data})

def Reply(request,rid):
    data=tbl_complaint.objects.get(id=rid)  
    if request.method=='POST':
        reply=request.POST.get("reply")
        data.comp_reply=reply
        data.comp_status=1
        data.save()
        return redirect('SiteAdm:Repliedcomplaints')
    else:
        return render(request,"SiteAdm/Reply.html") 

def Repliedcomplaints(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_complaint.objects.all()
    return render(request,"SiteAdm/Repliedcomplaints.html",{"repcomp":data})  

def Viewallusers(request):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_user.objects.all()
    for user in data:
        try:
            latitude = float(user.user_latitude)
            longitude = float(user.user_longitude)
            # Attach location_name as an attribute to each user object
            user.location_name = get_location_name(latitude, longitude)
        except ValueError as e:
            print(f"Error converting latitude/longitude for user {user.id}: {e}")
            user.location_name = "Unknown"  # Handle users with invalid coordinates

    return render(request, "SiteAdm/Viewallusers.html", {"user": data})


def Viewusertooldetails(request,uid):
    if "admid" not in request.session:
        return redirect("Guest:Login")
    utooldata=tbl_tool.objects.filter(user=uid)
    urentdata=tbl_renttool.objects.filter(user=uid)
    urentaldata=tbl_renttool.objects.filter(tool__user=uid)
    return render(request,"SiteAdm/Viewusertooldetails.html",{"utool":utooldata,"urent":urentdata,"urental":urentaldata})

def blockuser(request,id, status):
    data=tbl_user.objects.get(id=id)
    data.user_status=status
    data.save()
    return redirect('SiteAdm:Viewallusers')
