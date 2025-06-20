from django.urls import path,include
from User import views
app_name='User'

urlpatterns=[
        path('',views.HomePage, name="HomePage"),

         path('Myprofile/',views.Myprofile,name="Myprofile"),
        path('Editprofile/',views.Editprofile,name="Editprofile"),
        path('Changepassword/',views.Changepassword,name="Changepassword"),

        path('Tool/',views.Tool,name="Tool"),
        # path('Viewtools/',views.Viewtools,name="Viewtools"),
        path('Rentdetails/<int:tid>',views.Rentdetails,name="Rentdetails"),

        path('bookmark/<int:tid>/<str:key>',views.bookmark,name="bookmark"),
        path('Viewbookmarks/',views.Viewbookmarks,name="Viewbookmarks"),
        path('deletebookmark/<int:did>/<str:key>',views.deletebookmark,name="deletebookmark"),
        
        path('deletetool/<int:did>',views.deletetool,name="deletetool"),
        path('edittool/<int:eid>',views.edittool,name="edittool"),
        path('Gallery/<int:tid>',views.Gallery,name="Gallery"),
        path('delete-image/<int:image_id>/', views.DeleteImage, name='DeleteImage'),

        path('Mybooking/',views.Mybooking,name="Mybooking"),
        path('Viewbooking/',views.Viewbooking,name="Viewbooking"),
        path('returned/<int:ret_id>',views.returned,name="returned"),
        
        path('Payment/<int:id>',views.Payment,name="Payment"),
        path('Payment_suc/',views.Payment_suc,name="Payment_suc"),
        path('Loader/',views.Loader,name="Loader"),

        path('Complaint/',views.Complaint,name="Complaint"),

        path('rating/<int:mid>',views.rating,name="rating"),  
        path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
        path('starrating/',views.starrating,name="starrating"),

        path('chatpage/<int:id>',views.chatpage,name="chatpage"),
        path('ajaxchat/',views.ajaxchat,name="ajaxchat"),
        path('ajaxchatview/',views.ajaxchatview,name="ajaxchatview"),
        path('clearchat/',views.clearchat,name="clearchat"),

        path('ajaxsearchtool/',views.ajaxsearchtool,name="ajaxsearchtool"),
        path('ajaxcancelbooking/',views.ajaxcancelbooking,name="ajaxcancelbooking"),
        path('reportdamage/<int:id>/<int:status>',views.reportdamage,name="reportdamage"),

]