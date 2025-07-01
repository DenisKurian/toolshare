from django.shortcuts import render,redirect
from User.models import *
from Guest.models import *
from datetime import datetime, date
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Avg
from django.db.models import Sum
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Count
from django.db.models import F
from geopy.geocoders import Nominatim
from django.core.paginator import Paginator
import math
import os

def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="ToolShareApp", timeout=100)
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address

def HomePage(request):
    catdata=None
    datas=None
    ar=None
    parry=None
    bookmark=None
    distances=None
    tool_lat=None
    tool_lon=None
    user_lat=None
    user_lon=None
    if 'uid' in request.session:
        tools = tbl_tool.objects.filter().exclude(user=request.session["uid"])
        is_authenticated = True
        catdata=tbl_category.objects.all()
        ar = [1, 2, 3, 4, 5]
        parry = []
        bookmark = []
        distances = []

        # Check for current location from query parameters
        user_lat = request.GET.get("lat")
        user_lon = request.GET.get("lon")
        if user_lat and user_lon:
            try:
                user_lat = float(user_lat)
                user_lon = float(user_lon)
            except ValueError:
                return render(request, "User/HomePage.html", {"error": "Invalid location parameters."})
        else:
            try:
                current_user = tbl_user.objects.get(id=request.session["uid"])
                user_lat = float(current_user.user_latitude)
                user_lon = float(current_user.user_longitude)
            except (tbl_user.DoesNotExist, ValueError):
                return render(request, "User/Homepage.html", {"error": "Unable to determine your location."})

        data = tbl_tool.objects.filter().exclude(user__id=request.session["uid"]).select_related("user")

        tools_with_distance = []
        for tool in data:
            try:
                tool_lat = float(tool.user.user_latitude)
                tool_lon = float(tool.user.user_longitude)
                distance = haversine(user_lat, user_lon, tool_lat, tool_lon)
                distance = round(distance, 2)  # Normal distance
            except ValueError:
                distance = None  # Use None for invalid coordinates instead of float("inf")

            ratecount = tbl_rating.objects.filter(tool=tool.id).count()
            if ratecount > 0:
                avg_rating = tbl_rating.objects.filter(tool=tool.id).aggregate(Avg("rating_data"))["rating_data__avg"]
                parry.append(math.floor(avg_rating))
                m= round(avg_rating) if avg_rating is not None else 0  # Ensure avg_rating is valid
            else:
                m=0
                parry.append(0)  # No ratings, default to 0
    

            print(f"Tool ID: {tool.id}, Average Rating (m): {m}")

            bmark = tbl_bookmark.objects.filter(user__id=request.session["uid"], tool=tool.id).first()
            bookmark.append(bmark.id if bmark else 0)

            distances.append(distance)  # None for invalid, otherwise rounded distance
            tools_with_distance.append((tool, distance if distance is not None else float("inf")))
        print(tools_with_distance)
        tools_with_distance.sort(key=lambda x: x[1])
        sorted_tools = []
        sorted_parry = []
        sorted_bookmark = []
        sorted_distances = []
        for tool, dist in tools_with_distance:
            tool_index = [t.id for t in data].index(tool.id)  # Match tool by ID
            sorted_tools.append(tool)
            sorted_parry.append(parry[tool_index])
            sorted_bookmark.append(bookmark[tool_index])
            sorted_distances.append(dist)

        datas = zip(sorted_tools, sorted_parry, sorted_bookmark, sorted_distances)
        

        context = {
        "datas": datas,
        "ar": ar,
        "cat": catdata,
        "user_location": {"latitude": user_lat, "longitude": user_lon},
        "is_authenticated": is_authenticated,
        
        
        
        }
    else:
        is_authenticated = False
        tools = tbl_tool.objects.all()
       
        context = {
            "datas": datas,
            "ar": ar,
            "cat": catdata,
            "user_location": {"latitude": user_lat, "longitude": user_lon},
            "is_authenticated": is_authenticated,
            "tools": tools
            
        }
    return render(request,"User/HomePage.html", context)

def Editprofile(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_user.objects.get(id=request.session['uid'])
    if request.method=='POST':
        uname=request.POST.get('txtname')
        uemail=request.POST.get('txtemail')
        ucontact=request.POST.get('txtcontactno')
        # lat=request.POST.get("latitude")
        # long=request.POST.get("longitude")
        if tbl_user.objects.filter(user_name=uname).exclude(id=request.session['uid']).exists():
            return render(request, "User/Editprofile.html", {'msg': "Username already exists", 'profeddata': data})
        # Check if the new email already exists in the database
        if tbl_user.objects.filter(user_email=uemail).exclude(id=request.session['uid']).exists():
            return render(request, "User/Editprofile.html", { 'msg': "Email already exists",'profeddata': data,})
        data.user_name=uname
        data.user_email=uemail
        data.user_contact=ucontact
        # data.user_latitude=lat
        # data.user_longitude=long
        # Update location **only if user allows**
        if request.POST.get("update_location") == "on":
            lat=request.POST.get("latitude")
            long=request.POST.get("longitude")
            if lat and long:
                data.user_latitude = lat
                data.user_longitude = long

        # Update images only if a new file is uploaded
        if 'fphoto' in request.FILES:
            data.user_photo = request.FILES['fphoto']
        if 'fproof' in request.FILES:
            data.user_proof = request.FILES['fproof']
        # data.user_photo=request.FILES.get('fphoto')
        # data.user_proof=request.FILES.get('fproof')
        # Check if the new username already exists in the database
        
        data.save()
        return redirect('User:Myprofile')
    else:
        return render(request,"User/Editprofile.html",{'profeddata':data})

def Myprofile(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_user.objects.get(id=request.session['uid'])
    tools = tbl_tool.objects.filter(user=request.session['uid'])
    
    
    catdata=tbl_category.objects.all()
    ar = [1, 2, 3, 4, 5]
    parry = []
    
    

    

    

    
    for tool in tools:
        

        ratecount = tbl_rating.objects.filter(tool=tool.id).count()
        if ratecount > 0:
            avg_rating = tbl_rating.objects.filter(tool=tool.id).aggregate(Avg("rating_data"))["rating_data__avg"]
            parry.append(math.floor(avg_rating))
        else:
            parry.append(0)

        

        

    # Sort tools by distance (None values will go to the end via float("inf"))

    

    sorted_tools = []
    sorted_parry = []
    

    for tool in tools:
        tool_index = [t.id for t in tools].index(tool.id)  # Match tool by ID
        sorted_tools.append(tool)
        sorted_parry.append(parry[tool_index])
    


    datas = zip(sorted_tools, sorted_parry)


    return render(request, "User/Myprofile.html", {
        "user": data,
        "tool": datas,
        "ar": ar,
        "cat": catdata,
        
    })
    



def Changepassword(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_user.objects.get(id=request.session['uid'])
    dbpass=data.user_password
    if request.method=='POST':
        oldpass=request.POST.get('txtoldpassword')
        newpass=request.POST.get('txtnewpassword')
        confirmpass=request.POST.get('txtconfirmpassword')  
        if check_password(oldpass, dbpass):  # Verify the password
            if newpass==confirmpass:
                newpass = make_password(request.POST.get("txtnewpassword")) # Encrypt the password
                data.user_password=newpass
                data.save()
                return render(request,"User/Changepassword.html",{'msg1':'Password updated'})
            else:
                return render(request,"User/Changepassword.html",{'msg':'Password does not match'})
        else:
            return render(request,"User/Changepassword.html",{'msg':'Incorrect current password '})
    else:
        return render(request,"User/Changepassword.html")

def Tool(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_tool.objects.filter(user=request.session['uid'])
    userid=tbl_user.objects.get(id=request.session['uid'])
    cat=tbl_category.objects.all()
    if request.method=='POST':
        tname=request.POST.get('txttoolname')
        tdetails=request.POST.get('txtdetails')
        tppd=request.POST.get('txtprice')

        file=request.FILES.get('btnfile')
        tqty=request.POST.get('txtquantity')
        tdeposit=request.POST.get('txtdeposit')
        categoryid=tbl_category.objects.get(id=request.POST.get('sel category'))
        tbl_tool.objects.create(tool_name=tname,tool_details=tdetails,tool_priceperday=tppd,user=userid,qty=tqty,tool_deposit=tdeposit,category=categoryid, gallery_file=file)
        return redirect('User:Tool')
    else:
        return render(request,"User/Tool.html",{'tool':data, 'cat':cat})

def deletetool(request,did):
    tool=tbl_tool.objects.get(id=did)
    if tbl_renttool.objects.filter(tool=tool).exists():
        return render(request,"User/Tool.html",{'msg':'Tool is already booked'})
    else:
        tbl_tool.objects.get(id=did).delete()
        return redirect('User:Tool')

def edittool(request,eid):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_tool.objects.get(id=eid)
    cat=tbl_category.objects.all()
    if request.method=='POST':
        tname=request.POST.get('txttoolname')
        tdetails=request.POST.get('txtdetails')
        tppd=request.POST.get('txtprice')
        tdep=request.POST.get('txtdeposit')
        category=tbl_category.objects.get(id=request.POST.get('sel category'))
        qty=request.POST.get('txtquantity')
        #data.gallery_file=request.FILES.get('btnfile')
        if 'btnfile' in request.FILES:
            data.gallery_file = request.FILES['btnfile']
        data.tool_deposit=tdep
        data.tool_name=tname
        data.tool_details=tdetails
        data.tool_priceperday=tppd
        data.qty=qty
        data.category=category
        data.save()
        return redirect('User:Myprofile')
    else:
        return render(request,"User/edittool.html",{'tooled':data, 'cat':cat})

def Gallery(request,tid):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    tool=tbl_tool.objects.get(id=tid)
    gallery_images = tbl_gallery.objects.filter(tool_id=tid)  # Fetch all images for the tool
    if request.method=='POST':
        file=request.FILES.get('btnfile')
        if file:
            tbl_gallery.objects.create(gallery_image=file, tool_id=tool.id)
        return redirect('User:Gallery', tid)
    else:
        return render(request,"User/Gallery.html", {'tool':tool, 'gallery_images':gallery_images})  

from django.shortcuts import get_object_or_404, redirect
from .models import tbl_gallery

def DeleteImage(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(tbl_gallery, id=image_id)
        tool_id = image.tool.id  # Store the tool ID to redirect back to the appropriate page
        image.delete()
        return redirect('User:Gallery', tid=tool_id)  # Redirect back to the Rentdetails page
    return HttpResponse(status=405)  # Method Not Allowed

def Complaint(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    userid=tbl_user.objects.get(id=request.session['uid'])
    data=tbl_complaint.objects.filter(user=userid)
    if request.method=='POST':
        title=request.POST.get('txttitle')
        content=request.POST.get('txtcontent')
        tbl_complaint.objects.create(comp_title=title,comp_content=content,user=userid)
        return redirect('User:Complaint')
    else:
        return render(request,"User/Complaint.html",{'comp':data})
    


def Rentdetails(request, tid):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data = tbl_tool.objects.get(id=tid)
    userid = tbl_user.objects.get(id=request.session['uid'])
    amount = float(data.tool_priceperday)
    deposit = int(data.tool_deposit)
    total_qty = data.qty
    bookings = tbl_renttool.objects.filter(
        tool=data,
        rent_tool_status__in=[0, 1]
    ).values('rent_tool_fromdate', 'rent_tool_todate', 'rent_tool_qty')
    booked_ranges = [
        {
            'from': booking['rent_tool_fromdate'].isoformat(),
            'to': booking['rent_tool_todate'].isoformat(),
            'qty': booking['rent_tool_qty']
        } for booking in bookings
    ]
    gallery_images = tbl_gallery.objects.filter(tool_id=tid)
    
    try:
        latitude = float(data.user.user_latitude)
        longitude = float(data.user.user_longitude)
        # Attach location_name as an attribute to each user object
        data.user.location_name = get_location_name(latitude, longitude)
    except ValueError as e:
        print(f"Error converting latitude/longitude for user {data.user.id}: {e}")
        data.user.location_name = "Unknown"  # Handle users with invalid coordinates
    
    if request.method == 'POST':
        try:
            fromdate_str = request.POST.get('from_date')
            todate_str = request.POST.get('to_date')
            qty_requested = int(request.POST.get('txtquantity', 1))
            if qty_requested <= 0:
                raise ValueError("Quantity must be greater than 0")
            if qty_requested > total_qty:
                raise ValueError(f"Requested quantity ({qty_requested}) exceeds total available ({total_qty})")
            fromdate = datetime.strptime(fromdate_str, '%Y-%m-%d')
            todate = datetime.strptime(todate_str, '%Y-%m-%d')
            if todate < fromdate:
                raise ValueError("End date must be after start date")
            overlapping_bookings = tbl_renttool.objects.filter(
                tool=data,
                rent_tool_status__in=[0, 1],
                rent_tool_fromdate__lte=todate,
                rent_tool_todate__gte=fromdate
            ).aggregate(total_booked=Sum('rent_tool_qty'))['total_booked'] or 0
            available_qty = total_qty - overlapping_bookings
            if available_qty >= qty_requested:
                diff = (todate - fromdate).days + 1
                days = max(diff, 1)
                total = (amount * days * qty_requested) + int(data.tool_deposit)    
                rentT = tbl_renttool.objects.create(
                    rent_tool_fromdate=fromdate,
                    rent_tool_todate=todate,
                    user=userid,
                    tool=data,
                    rent_tool_price=total,
                    rent_tool_qty=qty_requested
                )
                return redirect('User:Payment',rentT.id)
            else:
                return render(request, "User/Rentdetails.html", {
                    "amount": amount,
                    "deposit": deposit,
                    "booked_ranges": booked_ranges,
                    "tool_id": tid,
                    "total_qty": total_qty,
                    "available_qty": available_qty, 
                    "error": f"Only {available_qty} units available for the selected dates",
                    "gallery_images": gallery_images,
                    "data":data

                })
                
        except ValueError as e:
            return render(request, "User/Rentdetails.html", {
                "amount": amount,
                "deposit": deposit,
                "booked_ranges": booked_ranges,
                "tool_id": tid,
                "total_qty": total_qty,
                "error": str(e),
                "gallery_images": gallery_images,
                "data":data
            })
    overlapping_bookings = tbl_renttool.objects.filter(
        tool=data,
        rent_tool_status__in=[0, 1]
    ).aggregate(total_booked=Sum('rent_tool_qty'))['total_booked'] or 0
    available_qty = total_qty - overlapping_bookings
    return render(request, "User/Rentdetails.html", {
       "amount": amount,
        "deposit": deposit,
        "booked_ranges": booked_ranges,
        "tool_id": tid,
        "total_qty": total_qty,
        "available_qty": available_qty,
        "gallery_images": gallery_images,
        "data":data
    })

def ajaxcancelbooking(request):
    rent = tbl_renttool.objects.get(id=request.GET.get('id'))
    dates = date.today()
    fromdate = rent.rent_tool_fromdate
    diff = (fromdate - dates).days
    dept = rent.tool.tool_deposit
    totalamount = rent.rent_tool_price
    amount = float(totalamount) - int(dept)
    if diff == 1:
        cancelamount = amount * 0.3
        rent.cancel_fee = cancelamount
        rent.save()
    elif diff >= 2 and diff <= 5:
        cancelamount = amount * 0.2
        rent.cancel_fee = cancelamount
        rent.save()
    else:
        cancelamount = amount * 0.1
        rent.cancel_fee = cancelamount
        rent.save()
    rent.rent_tool_status=3
    rent.save()
    return JsonResponse({"msg":"Booking Cancelled Successfully"})




def bookmark(request,tid,key):
    data=tbl_tool.objects.get(id=tid)
    tbl_bookmark.objects.create(tool=data,user=tbl_user.objects.get(id=request.session['uid']))
    if key=='datas':
        return redirect('User:HomePage')
    else:
        return redirect('User:Viewbookmarks')

def deletebookmark(request,did,key):
    tbl_bookmark.objects.get(id=did).delete()
    if key=='datas':
        return redirect('User:HomePage')
    else:
        return redirect('User:Viewbookmarks')

from django.db.models import Avg
import math

def Viewbookmarks(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    
    bmark = tbl_bookmark.objects.filter(user=request.session['uid'])
    catdata = tbl_category.objects.all()
    ar = [1, 2, 3, 4, 5]
    parry = []

    # Calculate ratings for each bookmark
    for bookmark in bmark:
        tool_id = bookmark.tool.id
        avg_rating = tbl_rating.objects.filter(tool=tool_id).aggregate(Avg("rating_data"))["rating_data__avg"]
        parry.append(math.floor(avg_rating)) if avg_rating is not None else parry.append(0)

    # Align sorted tools and ratings
    sorted_tools = []
    sorted_parry = []
    for tool, rating in zip(bmark, parry):  # Use zip to ensure alignment
        sorted_tools.append(tool)
        sorted_parry.append(rating)

    # Zip final sorted tools with ratings
    bm = zip(sorted_tools, sorted_parry)

    return render(request, "User/Viewbookmarks.html", {
        "bm": bm,
        "ar": ar,
        "cat": catdata,
    })

def Mybooking(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data = tbl_renttool.objects.filter(user=request.session['uid'])
    today = date.today().isoformat()

    bookings = []
    for i in data:
        fromdate = i.rent_tool_fromdate.isoformat()
        bookings.append({"data": i, "fromdate": fromdate})
    return render(request, "User/Mybooking.html", {"bookings": bookings, "tdy": today})

def Viewbooking(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    data=tbl_renttool.objects.filter(tool__user=request.session['uid'])
    return render(request,"User/Viewbooking.html",{"book":data})

def returned(request,ret_id):
    data=tbl_renttool.objects.get(id=ret_id)
    dates = date.today()
    deposit = data.tool.tool_deposit
    todate = data.rent_tool_todate
    diff = (todate - dates).days
    if diff == 0:
        latefee = 0
        data.late_fee = latefee
        data.save()
    elif diff >=1 and diff <= 2:
        latefee = deposit * 0.1
        data.late_fee = latefee
        data.save()
    elif diff >= 3 and diff <= 5:
        latefee = deposit * 0.2
        data.late_fee = latefee
        data.save()
    else:
        latefee = deposit 
        data.late_fee = latefee
        data.save()        
    data.rent_tool_status=2
    data.save()
    return redirect('User:Viewbooking') 



def rating(request,mid):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    parray=[1,2,3,4,5]
    mid=mid
    counts=0
    counts=stardata=tbl_rating.objects.filter(tool=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(tool=mid).order_by('-rating_datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        return render(request,"User/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
            return render(request,"User/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    user_id=tbl_user.objects.get(id=request.session['uid'])
    rating_review=request.GET.get('rating_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=user_id,rating_review=rating_review,rating_data=rating_data,tool=tbl_tool.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(tool=pid).order_by('-rating_datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(tool=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(tool=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)


def chatpage(request,id):
    user  = tbl_user.objects.get(id=id)
    return render(request,"User/Chat.html",{"user":user})

def ajaxchat(request):
    from_user = tbl_user.objects.get(id=request.session["uid"])
    to_user = tbl_user.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),user_from=from_user,user_to=to_user,chat_file=request.FILES.get("file"))
    return render(request,"User/Chat.html")

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_user.objects.get(id=request.session["uid"])
    chat_data = tbl_chat.objects.filter((Q(user_from=user) | Q(user_to=user)) & (Q(user_from=tid) | Q(user_to=tid))).order_by('chat_time')
    return render(request,"User/ChatView.html",{"data":chat_data,"tid":int(tid)})

def clearchat(request):
    tbl_chat.objects.filter(Q(user_from=request.session["uid"]) & Q(user_to=request.GET.get("tid")) | (Q(user_from=request.GET.get("tid")) & Q(user_to=request.session["uid"]))).delete()
    return render(request,"User/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def ajaxsearchtool(request):
    ar = [1, 2, 3, 4, 5]
    parry = []
    bookmark = []
    distances = []

    # Check for current location from query parameters
    user_lat = request.GET.get("lat")
    user_lon = request.GET.get("lon")

    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
        except ValueError:
            return render(request, "User/Homepage.html", {"error": "Invalid location parameters."})
    else:
        try:
            current_user = tbl_user.objects.get(id=request.session["uid"])
            user_lat = float(current_user.user_latitude)
            user_lon = float(current_user.user_longitude)
        except (tbl_user.DoesNotExist, ValueError):
            return render(request, "User/HomePage.html", {"error": "Unable to determine your location."})
    if request.GET.get("catid") != "" and request.GET.get("name") != "":
        data = tbl_tool.objects.filter(category=request.GET.get("catid"),tool_name__istartswith=request.GET.get("name")).exclude(user__id=request.session["uid"]).select_related("user")
    elif request.GET.get("catid") != "":
        data = tbl_tool.objects.filter(category=request.GET.get("catid")).exclude(user__id=request.session["uid"]).select_related("user")
    elif request.GET.get("name") != "":
        data = tbl_tool.objects.filter(tool_name__istartswith=request.GET.get("name")).exclude(user__id=request.session["uid"]).select_related("user")
    else:
        data = tbl_tool.objects.filter().exclude(user__id=request.session["uid"]).select_related("user")
    tools_with_distance = []
    for tool in data:
        try:
            tool_lat = float(tool.user.user_latitude)
            tool_lon = float(tool.user.user_longitude)
            distance = haversine(user_lat, user_lon, tool_lat, tool_lon)
            distance = round(distance, 2)  # Normal distance
        except ValueError:
            distance = None  # Use None for invalid coordinates instead of float("inf")

        ratecount = tbl_rating.objects.filter(tool=tool.id).count()
        if ratecount > 0:
            avg_rating = tbl_rating.objects.filter(tool=tool.id).aggregate(Avg("rating_data"))["rating_data__avg"]
            n=int(math.floor(avg_rating))
            print(n)
            parry.append(n)
        else:
            parry.append(0)

        bmark = tbl_bookmark.objects.filter(user__id=request.session["uid"], tool=tool.id).first()
        bookmark.append(bmark.id if bmark else 0)

        distances.append(distance)  # None for invalid, otherwise rounded distance
        tools_with_distance.append((tool, distance if distance is not None else float("inf")))  # Use inf for sorting

    # Sort tools by distance (None values will go to the end via float("inf"))
    tools_with_distance.sort(key=lambda x: x[1])
    sorted_tools = []
    sorted_parry = []
    sorted_bookmark = []
    sorted_distances = []

    for tool, dist in tools_with_distance:
        tool_index = [t.id for t in data].index(tool.id)  # Match tool by ID
        sorted_tools.append(tool)
        sorted_parry.append(parry[tool_index])
        sorted_bookmark.append(bookmark[tool_index])
        sorted_distances.append(dist)

    datas = zip(sorted_tools, sorted_parry, sorted_bookmark, sorted_distances)
    return render(request, "User/AjaxSearchTool.html", {
        "tool": datas,
        "ar": ar,
        "user_location": {"latitude": user_lat, "longitude": user_lon}
    })


def Payment(request,id):
   booking = tbl_renttool.objects.get(id=id)
   amount = booking.rent_tool_price
   if request.method == "POST":
      booking.rent_tool_status = 1
      booking.save()
      return redirect("User:Loader")
   else:
      return render(request,"User/Payment.html", {"total":amount})

def Loader(request):
    return render(request,"User/Loader.html")

def Payment_suc(request):
    return render(request,"User/Payment_suc.html")

def reportdamage(request,id,status):
    data=tbl_renttool.objects.get(id=id)
    data.rent_tool_status=status
    data.save()
    return redirect('User:Viewbooking')