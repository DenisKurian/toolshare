from django.urls import path,include
from SiteAdm import views
app_name = 'SiteAdm'

urlpatterns = [
    path('HomePage/',views.HomePage, name="HomePage"),

    path('Viewallusers/',views.Viewallusers, name="Viewallusers"),
    path('Viewusertooldetails/<int:uid>',views.Viewusertooldetails, name="Viewusertooldetails"),
    path('blockuser/<int:id>/<int:status>',views.blockuser, name="blockuser"),    

    path('Viewcomplaint/',views.Viewcomplaint, name="Viewcomplaint"),
    path('Repliedcomplaints/',views.Repliedcomplaints, name="Repliedcomplaints"),

    path('Reply/<int:rid>',views.Reply, name="Reply"),

    path('Category/',views.Category, name="Category"),
    path('deletecat/<int:did>',views.deletecat, name="deletecat"),
    path('editcat/<int:eid>',views.editcat, name="editcat"),

    path('AdminRegistration/',views.AdminRegistration, name="AdminRegistration"),
    path('deleteadmin/<int:did>',views.deleteadmin, name="deleteadmin"),
    path('editadmin/<int:eid>',views.editadmin, name="editadmin"),
]
