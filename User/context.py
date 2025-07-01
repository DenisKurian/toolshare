from .models import tbl_bookmark, tbl_renttool
from .models import tbl_tool, tbl_rating
from geopy.geocoders import Nominatim
from Guest.models import tbl_user
from django.db.models import Avg
import random
import math


def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="ToolShareApp", timeout=100)
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address

# def current_location(request):
#     your_loc=None
#     print("DEBUG: Context Processor Running...")
    
#         # Check for current location from query parameters
#     user_lat = request.GET.get("lat")
#     user_lon = request.GET.get("lon")
#     if user_lat and user_lon:
#         try:
#             user_lat = float(user_lat)
#             user_lon = float(user_lon)
#             your_loc=get_location_name(user_lat,user_lon)
            
#         except ValueError:
#             pass
#         try:
#             current_user = tbl_user.objects.get(id=request.session["uid"])
#             user_lat = float(current_user.user_latitude)
#             user_lon = float(current_user.user_longitude)
#             your_loc=get_location_name(user_lat,user_lon)
            
#         except (tbl_user.DoesNotExist, ValueError):
#             pass
#     return {
#             'your_loc': your_loc
#             }
            
def location_context_processor(request):
    if 'uid' in request.session:
        user_id = request.session['uid']
        try:
            user = tbl_user.objects.get(id=user_id)

            latitude = float(user.user_latitude)
            longitude = float(user.user_longitude)
            location_name = get_location_name(latitude, longitude)
            return {
                'location_name': location_name
            }
           
        except user.DoesNotExist:
            print(f"User with id {user_id} does not exist.")
            return {}
        except ValueError as e:
            print(f"Error converting latitude/longitude: {e}")
            return {}
    return {}
def tool_ratings(request):
    ar = [1, 2, 3, 4, 5]
    data = tbl_tool.objects.all()
    parry = []

    for tool in data:
        tot = 0
        ratecount = tbl_rating.objects.filter(tool=tool.id).count()
        if ratecount > 0:
            ratedata = tbl_rating.objects.filter(tool=tool.id)
            for rate in ratedata:
                tot += rate.rating_data
            avg = tot // ratecount
            parry.append(avg)
        else:
            parry.append(0)
    
    datas = zip(data, parry)
    return {'tools_with_ratings': datas, 'ar': ar}
def other_tools_ratings(request):
    if 'uid' in request.session:
        user_id = request.session['uid']
        ar = [1, 2, 3, 4, 5]
        data = tbl_tool.objects.exclude(user=user_id)
        parry = []

        for tool in data:
            tot = 0
            ratecount = tbl_rating.objects.filter(tool=tool.id).count()
            if ratecount > 0:
                ratedata = tbl_rating.objects.filter(tool=tool.id)
                for rate in ratedata:
                    tot += rate.rating_data
                avg = tot // ratecount
                parry.append(avg)
            else:
                parry.append(0)
        
        other_tools_ratings = list(zip(data, parry))
        random.shuffle(other_tools_ratings)

        return {'other_tools_ratings': other_tools_ratings, 'ar': ar}
    return {'other_tools_ratings': [], 'ar': []}
def mybooking_tools_ratings(request):
    if 'uid' in request.session:
       
        ar = [1, 2, 3, 4, 5]
        data=tbl_renttool.objects.filter(tool__user=request.session['uid'])
        parry = []

        for tool in data:
            tot = 0
            ratecount = tbl_rating.objects.filter(tool=tool.id).count()
            if ratecount > 0:
                ratedata = tbl_rating.objects.filter(tool=tool.id)
                for rate in ratedata:
                    tot += rate.rating_data
                avg = tot / ratecount  # Ensure floating-point division
                parry.append(avg)
            else:
                parry.append(0)
        
        mybooking_tools_ratings = zip(data, parry)
        return {'mybooking_tools_ratings': mybooking_tools_ratings, 'ar': ar}
    return {'mybooking_tools_ratings': [], 'ar': []}

def Viewbooking_tools_ratings(request):
    if 'uid' in request.session:
        user_id = request.session['uid']
        ar = [1, 2, 3, 4, 5]
        data=tbl_renttool.objects.filter(user=user_id)
        parry = []

        for tool in data:
            tot = 0
            ratecount = tbl_rating.objects.filter(tool=tool.id).count()
            if ratecount > 0:
                ratedata = tbl_rating.objects.filter(tool=tool.id)
                for rate in ratedata:
                    tot += rate.rating_data
                avg = tot / ratecount  # Ensure floating-point division
                parry.append(avg)
            else:
                parry.append(0)
        
        Viewbooking_tools_ratings = zip(data, parry)
        return {'Viewbooking_tools_ratings': Viewbooking_tools_ratings, 'ar': ar}
    return {'Viewbooking_tools_ratings': [], 'ar': []}

def mybookmark_tools_ratings(request):
    if 'uid' in request.session:
        user_id = request.session['uid']
        ar = [1, 2, 3, 4, 5]
        data = tbl_bookmark.objects.filter(user=user_id)
        parry = []

        for tool in data:
            tot = 0
            ratecount = tbl_rating.objects.filter(tool=tool.id).count()
            if ratecount > 0:
                ratedata = tbl_rating.objects.filter(tool=tool.id)
                for rate in ratedata:
                    tot += rate.rating_data
                avg = tot / ratecount  # Ensure floating-point division
                parry.append(avg)
            else:
                parry.append(0)
        
        mybookmark_tools_ratings = zip(data, parry)
        return {'mybookmark_tools_ratings': mybookmark_tools_ratings, 'ar': ar}
    return {'mybookmark_tools_ratings': [], 'ar': []}


def user_tools_ratings(request):
    if 'uid' in request.session:
        user_id = request.session['uid']
        ar = [1, 2, 3, 4, 5]
        data = tbl_tool.objects.filter(user=user_id)
        parry = []

        for tool in data:

            ratecount = tbl_rating.objects.filter(tool=tool.id).count()
            if ratecount > 0:
                avg_rating = tbl_rating.objects.filter(tool=tool.id).aggregate(Avg("rating_data"))["rating_data__avg"]
                parry.append(round(avg_rating))
            else:
                parry.append(0)
            
        
        user_tools_ratings = zip(data, parry)
        return {'user_tools_ratings': user_tools_ratings, 'ar': ar}
    return {'user_tools_ratings': [], 'ar': []}
def tool_rating_details(request):
    tool_id = request.resolver_match.kwargs.get('tid')
    if tool_id:
        tool = tbl_tool.objects.get(id=tool_id)
        ratings = tbl_rating.objects.filter(tool=tool)
        total_rating = 0
        rating_count = ratings.count()
        if rating_count > 0:
            for rating in ratings:
                total_rating += rating.rating_data
            average_rating = math.floor(total_rating / rating_count)
        else:
            average_rating = 0
        
        return {
            'tool': tool,
            'ratings': ratings,
            'average_rating': average_rating,
            'rating_count': rating_count,
        }
    return {
        'tool': None,
        'ratings': [],
        'average_rating': 0,
        'rating_count': 0,
    }

def bookmark_status(request):
    if 'uid' in request.session:
        user_id = request.session['uid']
        bookmarks = tbl_bookmark.objects.filter(user_id=user_id)
    else:
        bookmarks = []
    return {'bookmarks': bookmarks}

def auth_status(request):
    is_authenticated = 'uid' in request.session
    admin_authenticated = 'admid' in request.session
    return {'is_authenticated': is_authenticated, 'admin_authenticated': admin_authenticated}