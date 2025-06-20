from django.db import models

class tbl_user(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.EmailField(max_length=50)
    user_password=models.CharField(max_length=50)
    user_proof=models.FileField(upload_to="profile/proof/")   
    user_photo=models.ImageField(upload_to="profile/", default="staticfiles/profiles/user-default.png", )
    user_contact=models.CharField(max_length=50)
    user_latitude=models.FloatField(max_length=50)
    user_longitude=models.FloatField(max_length=50)
    user_status=models.IntegerField(default=0)  
